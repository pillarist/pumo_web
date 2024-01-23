import machine
machine.freq(240000000)
import _thread
import time
from microdot import Microdot


app = Microdot()
btn_num_arr = [2,4,5,12,13,15,25,26,27]
def clearer():
    for i in range(1,2):
        pin = machine.Pin(i, machine.Pin.OUT)
        pin.off()


#_thread.start_new_thread(clearer,())

def csv_to_2d_array(data):
  rows = data.splitlines()
  array = []
  for row in rows:
    array.append([item for item in row.split(",")])
  return array


# html = open(r"{}\template\web_html.html".format(c_path),"r").read()
# table = open(r"{}\table_dir\day.csv".format(c_path),"r+")


html = open("/web_html.html","r").read()

def render_table(tab_file):
  
    arr = csv_to_2d_array(tab_file.read())
    string_table = ""

    num =1 

    for line in arr:
        string_table += ("<tr>\n")
        string_table +="<tr>\n <td> {} </td>".format(num)
        num+=1
        for word in line:
            string_table +=('<td> {} </td> \n'.format(word))
        if(len(line) >2):
            if(line[1].isdigit()):
                string_table += '<form action=/btn/{} method="post"> \n '.format(line[1])
                string_table += ('<td> <button name=rack_no{} type="submit"> Rack no {} </button> </td> \n').format(line[1],line[1])
                string_table += '</form> \n'

        else:
            string_table += '<td> No button </td> \n'
 
        string_table += ('</tr>\n')  

    #print(string_table)
    
    return html.replace('table_1',string_table)
        

def try_func():
    table = open('/day.csv','r')
    
    page = render_table(tab_file=table)
    #print("this is :",page)
    table.close()
    
    #return send_file(r"C:\workspace\pumo\esp_web\web_esp\web_html.html")
    #return jinja.Template("C:\workspace\pumo\esp_web\web_esp\web_html.html").render()
    return page,200,{'Content-Type': 'text/html'}


@app.route('/')
async def index(request):

    return try_func()
    

@app.route('/add_newitem', methods=['POST'])
async def send_data(request):
    try:
        table = open('/day.csv','a')
        new_item = [request.form['input_1'],request.form['input_2'],request.form['input_3'],request.form['input_4'],request.form['input_5'],request.form['input_6'],request.form['input_7'],request.form['input_8']]

        if(new_item[0] != ''):
           
        
            for item in new_item:
                table.write('{},'.format(item))
            table.write(' \n')
                
            table.flush()
            table.close()
                        
            print(f'Received data: {new_item}')
            return try_func()

    except Exception as e:
        print(f'Error processing data: {e}')
        return {'error': 'Failed to process data'}, 500
    

@app.route('/add', methods=['POST'])
async def add_qt(request):
    try:
        table = open('/day.csv','r+')
        new_item = [request.form['add_id'],request.form['add_qt']]

        new_arr =[]
         
        
        # table.write("{},".format(item))
        # table.write(' \n')
        content = csv_to_2d_array(table.read())
        table.close()
        for index in content:
            if(index[0] == new_item[0]):
                index[7]=str(int(index[7]) + int(new_item[1]))
            new_arr.append(index)
            
        table = open('/day.csv','w')
        
        for row in new_arr:
            row_string = ""
            for i, info in enumerate(row):
                if i > 0:
                    row_string += ","
                row_string += str(info)
            table.write(row_string + "\n")
           
        
        table.flush()
        table.close()
                    
        print(f'Received data: {new_item}')
        return try_func()
    except Exception as e:
       print(f'Error processing data: {e}')
       return {'error': 'Failed to process new data'}, 500
    

@app.route('/remove', methods=['POST'])
async def add_qt(request):
    try:
        table = open('/day.csv','r+')
        
        new_item = [request.form['rm_id'],request.form['rm_qt']]

        new_arr =[]
        # table.write("{},".format(item))
        # table.write(' \n')
        content = csv_to_2d_array(table.read())
        table.close()
        for index in content:
            if(index[0] == new_item[0]):
                index[7]=str(int(index[7]) - int(new_item[1]))
            new_arr.append(index)
            
        table = open('/day.csv','w')
        
        for row in new_arr:
                row_string = ""
                for i, info in enumerate(row):
                    if i > 0:
                        row_string += ","
                    row_string += str(info)
                table.write(row_string + "\n")

        table.flush()
        table.close()
                    
        print(f'Received data: {new_item}')
        return try_func()
    except Exception as e:
       print(f"Error processing data: {e}")
       return {'error': 'Failed to process new data'}, 500
    
def gpio_on(num):
    if(int(num)<10):
        light = machine.Pin(int(btn_num_arr[num-1]),machine.Pin.OUT)
        light.on()
        time.sleep(5)
        light.off()

@app.route('/btn/<num>', methods=['POST'])
async def add_qt(request,num):
    _thread.start_new_thread(gpio_on,(int(num),))

    
        
if __name__ == "__main__":
    
    import network
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect("KININDIA_WIFI","21hq5k6l")
    while not wifi.isconnected():
        pass
    print(wifi.ifconfig())
    host=wifi.ifconfig()[0]
    port=8081
    
    print(f"Starting server at http://{host}:{port}/")
    try:
        app.run(host=host, port=8081, debug=True)
    except:
        print("an error occured")
    finally:
        app.run(host=host, port=8081, debug=True)
