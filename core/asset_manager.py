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
from pathlib import Path
from core.source_manager import SourceManager
import json
class AssetManager():
    def __init__(self):
        self.asset_local_path_prefix = Path(".minecraft") / "assets" / "objects"
    def get_objects_list(self,asset_index_path,instance_path):
        with open (asset_index_path,"r",encoding="utf-8") as ai:
            asset_index=json.load(ai)
        objects=asset_index["objects"]
        objects_list=[]
        asset_url_prefix = SourceManager().get_download_source().get_asset_base_url()
        for name,mc_object in objects.items():
            object_hash=self.get_object_hash(mc_object)
            url=self.generate_object_url(asset_url_prefix,object_hash)
            path=self.generate_object_local_path(object_hash,instance_path)
            object_dict={"url":url,
                         "path":path,
                         "name":name,
                         "hash":object_hash}
            objects_list.append (object_dict)

        return objects_list

    def get_object_hash(self,object):
        object_hash=object["hash"]
        return object_hash
    def generate_object_url(self, asset_url_prefix, object_hash):
        url = f"{asset_url_prefix}/{object_hash[:2]}/{object_hash}"
        return url
    def generate_object_local_path(self,object_hash,instance_path):
        instance_path=Path(instance_path)
        local_path=instance_path / self.asset_local_path_prefix /str(object_hash[:2])/str(object_hash)
        return local_path 