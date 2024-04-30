import env_check
import sys
import  config

def main():
    pre_detect:dict = env_check.detect_os()
    if pre_detect["OS"] == 'Windows':
        return f"Under the development![-empty-]"
    if pre_detect["OS"] == 'Linux':
        return config.config()
    if pre_detect["OS"] == 'Unknown':
        return f"Unknown OS sorry this app is unavailable"

if __name__=="__main__":
    print(main())