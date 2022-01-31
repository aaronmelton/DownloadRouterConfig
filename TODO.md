# Running Pylint
************* Module download_router_config.download_router_config
download_router_config/download_router_config.py:13:0: E0401: Unable to import 'config' (import-error)
download_router_config/download_router_config.py:16:0: R0914: Too many local variables (18/15) (too-many-locals)
download_router_config/download_router_config.py:75:4: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
download_router_config/download_router_config.py:77:8: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
download_router_config/download_router_config.py:80:4: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
download_router_config/download_router_config.py:114:19: W0703: Catching too general exception Exception (broad-except)
download_router_config/download_router_config.py:120:4: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
download_router_config/download_router_config.py:121:4: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
download_router_config/download_router_config.py:123:4: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
download_router_config/download_router_config.py:16:0: R0915: Too many statements (53/50) (too-many-statements)

------------------------------------------------------------------
Your code has been rated at 8.08/10 (previous run: 8.08/10, +0.00)



# Validations
1. Validate backup_to directory exists; What to do if it doesn't?
2. Add argument to specify where to drop the summary log?