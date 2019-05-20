# for file paths

# FUNCTIONS DEPRECATED; USE CLASS INSTEAD

def uploadFolder():
    """Folder containing files that are uploaded"""
    return r"upload_command_files"

def worldInfo():
    """World info folder"""
    return r"upload_worldinfo"

def sinoaliceInfo():
    """SINoALICE translation folder"""
    return r"upload_sinoalice"

def tempFolder():
    """Folder for holding temporary files"""
    return r"tmp"

class Path:

    upload_folder = r"upload_command_files"
    world_info = r"upload_worldinfo"
    sinoalice_info = r"upload_sinoalice"
    temp_folder = r"tmp"
    gacha_folder = r"gacha"
    gacha_cache = r"gacha\gacha_cache"
