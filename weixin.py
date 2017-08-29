import itchat


if __name__== '__main__':
 
    itchat.auto_login(hotReload=True)
    # friends = itchat.get_friends(update=True)
    frined = itchat.search_friends(name='')
    print(frined[0]['UserName'])
    
    itchat.send('起来尿尿了', toUserName=frined[0]['UserName'])
    itchat.send('起来尿尿了', toUserName=frined[0]['UserName'])
    itchat.send('起来尿尿了', toUserName=frined[0]['UserName'])