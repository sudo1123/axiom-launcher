'''== 配置文件默认内容 == '''
TEMPLATES={
"config.json":{
    "config_version": 2,

    "launcher": {
        "name": "Axiom Launcher",
        "version": "0.4.0"
    },

    "minecraft": {
        "selected_instance": ""
    },

    "java": {
        "path": r"C:\path\to\java.exe",
        "memory": {
            "min": 1024,
            "max": 4096
        }
    },

    "game": {
        "resolution": {
            "width": 854,
            "height": 480
        },
        "fullscreen": "false"
    }
},

"launch_context.json":{
    "is_demo_user": False,

    "has_custom_resolution": False,

    "has_quick_plays_support": False,

    "is_quick_play_singleplayer": False,

    "is_quick_play_multiplayer": False,

    "is_quick_play_realms": False
},

"accounts.json":{
    "accounts": [
        {
            "id": "offline_default",
            "type": "offline",
            "username": "Steve"
        }
    ],

    "selected": "offline_default"
}
}