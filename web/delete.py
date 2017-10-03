import os
import config


def doIt( tlId, environ, start_response ) :
    print ("Deleting workdown "+ tlId)
    # print ("TALIDIR: "+config.TALIDIR+", WODODIR: "+config.WODODIR)
        
    # if not os.path.isdir( config.WODODIR+"/"+os.path.split(tlId)[0] ):
    #     os.makedirs(config.WODODIR+"/"+os.path.split(tlId)[0])
        
    # with open(config.WODODIR+"/"+tlId+"."+dt+".json", 'w') as fp:
    #     json.dump(jason_data, fp, indent=4)
    
    os.remove(config.WODODIR+"/"+tlId+".json")

    start_response('303 See Other', [('Location',config.CONTEXT+'/')])

    return ['1']
