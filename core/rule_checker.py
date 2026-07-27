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
import re
class RuleChecker:

    def __init__(self, runtime_context):
        self.runtime_context = runtime_context


    def check_rule(self, rule):

        # 检查 os 条件
        if "os" in rule:
            if not self.check_os(rule["os"]):
                return None

        # 检查 features 条件
        if "features" in rule:
            if not self.check_features(rule["features"]):
                return None

        # 条件全部满足
        return rule["action"]
        


    def check_os(self, os_rule):
        runtime_info={
            "name":self.runtime_context["os_name"],
            "version":self.runtime_context["os_version"],
            "arch":self.runtime_context["arch"]
            }
        for rule_key in os_rule:

            if rule_key not in runtime_info.keys(): #规则中有未知的键
                return False
            if rule_key == "version":    #特殊：系统版本号启用正则匹配
                if re.match(os_rule[rule_key], runtime_info[rule_key]) is None: #正则匹配失败
                    return False
            else: 
                if os_rule[rule_key] != runtime_info[rule_key]: #值不相等
                    return False
        return True


    def check_features(self, feature_rule):
        pass        #检查是否匹配特性，目前不重要暂时留空


    def check_rules(self, rule_list):

        result = False   # 默认不加载

        for rule in rule_list:

            action = self.check_rule(rule)

            if action is None:
                continue

            if action == "allow":
                result = True

            elif action == "disallow":
                result = False

            else:
                raise ValueError(f"未知action: {action}")

        return result