    # iApp macro engine for iRules: https://techdocs.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-iapps-developer-11-4-0/3.html
    defaults_iapp_macro_engine = dict(
        BLOCK_START_STRING    = '<%',
        BLOCK_END_STRING      = '%>',
        VARIABLE_START_STRING = '<%=',
        VARIABLE_END_STRING   = '%>',
        COMMENT_START_STRING  = '<#',  # iApp macro engine has no comment functionality
        COMMENT_END_STRING    = '#>',  # iApp macro engine has no comment functionality
    )
