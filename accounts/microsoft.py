# Axiom Launcher - a third-party Minecraft: Java Edition launcher
# Copyright (C) 2026  Felix Qu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
import time
import uuid
from accounts.account import Account
'''
【重要提示】【Azure Client ID 使用说明】

本项目中的 Azure Client ID 仅用于 Axiom Launcher 官方版本的 Microsoft 身份认证流程。

该 Client ID 属于 Axiom Launcher 官方 Azure 应用注册，不包含在 GPL v3 授权范围内。

如果您 Fork、修改或发布本项目的衍生版本，建议在 Azure 开发者平台注册并使用您自己的 Application Client ID，而不是继续依赖官方 Client ID。

未经授权，请勿将该 Client ID 用于与 Axiom Launcher 无关的第三方应用。

Axiom Launcher 项目保留管理、更新或撤销该 Client ID 的权利。
'''

CLIENT_ID="e19efb66-04cc-4cd0-87c4-afa20749b3f7"


DEVICE_CODE_URL="https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode"
TOKEN_URL="https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
XBL_AUTH_URL="https://user.auth.xboxlive.com/user/authenticate"
XSTS_AUTH_URL = "https://xsts.auth.xboxlive.com/xsts/authorize"
MC_LOGIN_URL = "https://api.minecraftservices.com/authentication/login_with_xbox"
MC_PROFILE_URL = "https://api.minecraftservices.com/minecraft/profile"

class MicrosoftAuthenticator:
    '''
    微软OAuth六步鉴权类
    '''
    def __init__(self):
        pass

    def authenticate_1(self):
        """
        鉴权总入口函数(第一部分)
        发起鉴权请求，要求用户去浏览器完成授权
        返回dict
        键名：
        user_code ：用户认证用的设备码短码
        device_code : 传入鉴权总入口函数(第二部分)的设备码长码
        verification_uri : 用户认证所要访问的网址
        interval : 认证限时


        """
        init_response=self.request_device_code()
        user_code=init_response["user_code"]
        device_code=init_response["device_code"]
        interval=init_response["interval"]
        verification_uri=init_response["verification_uri"]

        return {"user_code" :  user_code,
                "device_code" : device_code,
                "interval" : interval,
                "verification_uri" :verification_uri
        }

    def authenticate_2(self, device_code, interval):
        """
        鉴权总入口函数(第二部分)
        轮询用户授权结果，走完整鉴权链并返回账号字典

        返回dict键名：
        player_name, uuid, access_token, refresh_token,
        microsoft_token, xuid, client_id
        """
        # 1. 轮询换取微软 token（等待用户在浏览器授权）
        ms_token_dict = self.poll_for_token(device_code, interval)
        microsoft_token = ms_token_dict["access_token"]
        refresh_token = ms_token_dict["refresh_token"]

        # 2. 微软 token -> Xbox token -> XSTS token
        xbl_token, _ = self.get_xbox_token(microsoft_token)
        xsts_token, uhs = self.get_xsts_token(xbl_token)

        # 3. XSTS token -> Minecraft access_token
        mc_access_token = self.get_minecraft_token(xsts_token, uhs)

        # 4. 获取玩家档案
        player_name, player_id = self.get_profile(mc_access_token)

        # 5. 打包返回完整账号信息
        return {
            "player_name": player_name,
            "uuid": player_id,
            "access_token": mc_access_token,
            "refresh_token": refresh_token,
            "microsoft_token": microsoft_token,
            "xuid": uhs,
            "client_id": CLIENT_ID,
        }

    def refresh_microsoft_token(self,refresh_token):
        '''
        刷新用户信息方法
        注: refresh_token可由authenticate_2方法获得
        '''
        response=requests.post(TOKEN_URL,data={
        "grant_type":"refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token":refresh_token
        }
        )
        response.raise_for_status()
        return response.json()



    def request_device_code(self):
        response=requests.post(DEVICE_CODE_URL, 
                               data={
                                   "client_id": CLIENT_ID, 
                                    "scope": "XboxLive.signin offline_access"
                                    }
                                )

        response.raise_for_status()
        return response.json()

    def poll_for_token(self,device_code,interval,max_polling_time=300): #interval代表轮询间隔秒数
        poll_start_time=time.time()
        while (time.time()-poll_start_time) < max_polling_time: 
            response=requests.post(TOKEN_URL,data={
                    "grant_type":"urn:ietf:params:oauth:grant-type:device_code",
                    "client_id": CLIENT_ID,
                    "device_code" : device_code
                    }
                    )

            if response.status_code == 200:    #成功
                return response.json()

            error=response.json().get("error","") 

            if error == "authorization_pending":  #用户还没输码
                time.sleep(interval)              #间隔一会后再次请求
                continue
            if error == "authorization_declined": #用户拒绝
                print("检测到您在浏览器中点击了拒绝，正版账号绑定流程终止")
                return 
            if error == "expired_token" : #15分钟有效期已过
                print("当前设备码已过期，请您重新进行绑定流程")
                return
            if error == "bad_verification_code":
                raise ValueError("设备码无效")

            raise ValueError("未知error")

    def  get_xbox_token(self,microsoft_token):
        response=requests.post(XBL_AUTH_URL,json=
        {
            "Properties":{
                "AuthMethod":"RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket" : f"d={microsoft_token}",
                        },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        }
        )

        response.raise_for_status()
        xbl_token=response.json()["Token"]
        uhs=response.json()["DisplayClaims"]["xui"][0]["uhs"]

        return (xbl_token,uhs)

    def get_xsts_token(self, xbl_token):
        response=requests.post(XSTS_AUTH_URL,json=
        {
            "Properties":{
                "SandboxId": "RETAIL",
                "UserTokens": [xbl_token]
                        },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT"
        }
        )

        if response.status_code == 401:
            if response.json()["XErr"] == 2148916233:
                fail_reason="本账号未关联正版/未购买正版"
                raise PermissionError(fail_reason)
            raise PermissionError(f'XErr:{response.json()["XErr"]}')

        else: 
            response.raise_for_status()
            xsts_token=response.json()["Token"]
            uhs=response.json()["DisplayClaims"]["xui"][0]["uhs"]
    
            return (xsts_token,uhs)

    def get_minecraft_token(self,xsts_token,uhs):
        response=requests.post(MC_LOGIN_URL,json=
                {
                    "identityToken": f"XBL3.0 x={uhs};{xsts_token}"
                }
                )

        response.raise_for_status()

        return response.json()["access_token"]

    def get_profile(self,mc_access_token):
        headers={"Authorization":f"Bearer {mc_access_token}"}
        response=requests.get(MC_PROFILE_URL,
                              headers=headers,
                              timeout=30)
        response.raise_for_status()

        player_name=response.json()["name"]
        player_id=response.json()["id"]

        return player_name,player_id

class MicrosoftAccount(Account):
    """微软（正版）账号类"""

    def __init__(self, data):
        """
        data: authenticate_2 返回的账号信息字典
        键名: player_name, uuid, access_token, refresh_token,
            microsoft_token, xuid, client_id
        """
        super().__init__()
        # 基类字段
        self.auth_player_name = data["player_name"]
        self.auth_uuid = uuid.UUID(data["uuid"])     # 无横线字符串 -> UUID 对象
        self.auth_access_token = data["access_token"]
        self.user_type = "msa"                        # 正版标识，区别于 offline 的 legacy

        # 正版专属字段
        self.refresh_token = data["refresh_token"]
        self.microsoft_token = data["microsoft_token"]
        self.auth_xuid = data["xuid"]
        self.clientid = data["client_id"]
        self._authenticator = MicrosoftAuthenticator()


    def refresh(self):
        """刷新登录态：用 refresh_token 换新 token，重走鉴权链更新全部字段"""
        # 1. 刷新微软 token（拿到新的微软 token 和新的 refresh_token）
        new_token_dict = self._authenticator.refresh_microsoft_token(self.refresh_token)
        self.microsoft_token = new_token_dict["access_token"]
        self.refresh_token = new_token_dict["refresh_token"] 

        # 2. 重走鉴权链，刷新 Minecraft 层信息
        xbl_token, _ = self._authenticator.get_xbox_token(self.microsoft_token)
        xsts_token, uhs = self._authenticator.get_xsts_token(xbl_token)
        self.auth_access_token = self._authenticator.get_minecraft_token(xsts_token, uhs)
        player_name, player_id = self._authenticator.get_profile(self.auth_access_token)

        # 3. 更新玩家信息字段
        self.auth_player_name = player_name
        self.auth_uuid = uuid.UUID(player_id)
        self.auth_xuid = uhs

        return self