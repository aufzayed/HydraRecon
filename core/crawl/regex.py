endpoints_regex = r"""
  (?:"|')                               # Start newline delimiter
  (
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domain name (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domain extension and/or path
    |
    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    [^"'><,;|()]{1,})                   # Rest of the characters can't be
    |
    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/]{1,}                 # Resource name
    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
    |
    ([a-zA-Z0-9_\-/]{1,}/               # REST API (no extension) with /
    [a-zA-Z0-9_\-/]{3,}                 # Proper REST endpoints usually have 3+ chars
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
    |
    ([a-zA-Z0-9_\-]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json|
         action|html|js|txt|xml)        # . + extension
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
  )
  (?:"|')                               # End newline delimiter
"""
secrets_regex = \
    '''
    (xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}
    |
    https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}
    |
    [f|F][a|A][c|C][e|E][b|B][o|O][o|O][k|K].{0,30}['"\s][0-9a-f]{32}['"\s]
    |
    [t|T][w|W][i|I][t|T][t|T][e|E][r|R].{0,30}['"\s][0-9a-zA-Z]{35,44}['"\s]
    |
    [h|H][e|E][r|R][o|O][k|K][u|U].{0,30}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}|key-[0-9a-zA-Z]{32}
    |
    [0-9a-f]{32}-us[0-9]{1,2}
    |
    sk_live_[0-9a-z]{32}
    |
    [0-9(+-[0-9A-Za-z_]{32}.apps.qooqleusercontent.com
    |
    AIza[0-9A-Za-z-_]{35}
    |
    6L[0-9A-Za-z-_]{38}|ya29\.[0-9A-Za-z\-_]+
    |
    AKIA[0-9A-Z]{16}
    |
    amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}
    |
    s3\.amazonaws.com[/]+|[a-zA-Z0-9_-]*\.s3\.amazonaws.com|EAACEdEose0cBA[0-9A-Za-z]+
    |
    basic [a-zA-Z0-9_\-:\.]+
    |
    bearer [a-zA-Z0-9_\-\.]+|api[key|\s*]+[a-zA-Z0-9_\-]+
    |
    key-[0-9a-zA-Z]{32}|SK[0-9a-fA-F]{32}
    |
    AC[a-zA-Z0-9_\-]{32}|AP[a-zA-Z0-9_\-]{32}|access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}
    |
    sq0csp-[ 0-9A-Za-z\-_]{43}|sqOatp-[0-9A-Za-z\-_]{22}
    |
    sk_live_[0-9a-zA-Z]{24}
    |
    rk_live_[0-9a-zA-Z]{24}
    |
    [a-zA-Z0-9_-]*:[a-zA-Z0-9_\-]+@github\.com*
    |
    -----BEGIN PRIVATE KEY-----[a-zA-Z0-9\S]{100,}-----END PRIVATE KEY-----
    |
    -----BEGIN RSA PRIVATE KEY-----[a-zA-Z0-9\S]{100,}-----END RSA PRIVATE KEY-----
    |
    eyJ[a-zA-Z0-9]{10,}\.eyJ[a-zA-Z0-9]{10,}\.[a-zA-Z0-9_-]{10,})'''