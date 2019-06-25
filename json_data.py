import json,os
function="addstock"
name="xxx"
amount=10


#if os.path.exists('stock.json'):
#    os.remove('stock.json')


if function=="addstock":
    if not os.path.exists('stock.json'):
        print("no exists")
        with open('stock.json','w') as f:
            data_dict={name:amount}
            json.dump(data_dict,f)
            f.close()

    else:
        print("exists")
        with open('stock.json','r+') as f:
            data_update=json.load(f)
            f.close()
            print("before:",data_update)
            if name in data_update:
                data_update[name]+=amount
                print("after:",data_update)
                with open('stock.json','w',) as uf:
                    json.dump(data_update,uf)
                    uf.close()
