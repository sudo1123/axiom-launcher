from pathlib import Path
import json
class ConfigManager():
    def __init__(self):
        self.PROGRAM_DIR = Path(__file__).resolve().parent.parent
        self.config_file = self.PROGRAM_DIR / "configs" / "config.json"

    def load_config(self):
        path = Path(self.config_file)
        # 文件不存在，抛出错误
        if not path.exists():

            raise EnvironmentError("config加载失败，请检查配置文件")
        
        with open (path,"r", encoding="utf-8") as cf:
            return json.load(cf)

    
    def save_config(self, config):
        """
        保存config.json
        """

        with open(
            self.config_file,
            "w",
            encoding="utf-8"
        ) as cf:

            json.dump(
                config,
                cf,
                ensure_ascii=False,
                indent=4
            )

  


    def get_selected_instance(self):
        """
        获取当前选择的实例
        """
        config = self.load_config()
        selected_instance=config["minecraft"]["selected_instance"]

        return selected_instance



    def set_selected_instance(self, instance_id: str):
        """
        修改当前选择的实例
        """

        config = self.load_config()

        config["minecraft"]["selected_instance"] = instance_id

        self.save_config(config)