from config.settings import Config

if __name__ == '__main__':
    
    Config.create_block_from_env(block_name='config-bc-guatemala',env_path='guate.env',overwrite_block=True,override_env_vars=True)
    Config.create_block_from_env(block_name='config-bc-mexico',env_path='mex.env',overwrite_block=True,override_env_vars=True)