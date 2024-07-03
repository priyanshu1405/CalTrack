from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
import mysql.connector as my
from datetime import date, datetime
# mHYayv7eKmXcnXbHmeurag==ueCos82ZFg58qgsF

user = ''
m=my.connect(host="localhost",user="root",passwd="Sai_dbms",database="caltrack")
cursor=m.cursor()
myd = {}

def home(request):
    return render(request, 'home.html')

# Create your views here.
def mealadd(request):
    myd = {}
    print(user)
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    q_meals = "select * from meal where uname = '{}' and CAST(meal_date as date) = '{}'".format(user, formatted_date[0:10])
    cursor.execute(q_meals)
    records = cursor.fetchall()
    print(records)

    count = 1
    str_search = ''

    for i in records:
        str_search += i[2] + " and "

    query = str_search
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
    api_request = requests.get(api_url + query, headers = {'X-Api-Key': 'mHYayv7eKmXcnXbHmeurag==ueCos82ZFg58qgsF'})
    api = json.loads(api_request.content)

    count = 0
    
    bf = 1
    lh = 1
    sn = 1
    dn = 1
    for i in records:
        food = api[count]
        
        if i[1] == '1':
            
            myd['bsno{}'.format(bf)] = bf
            myd['bmeal{}'.format(bf)] = i[2]
            myd['bcal{}'.format(bf)] = food['calories']*i[3]/food['serving_size_g']
            bf+=1
        elif i[1] == '2':
            myd['lsno{}'.format(lh)] = lh
            myd['lmeal{}'.format(lh)] = i[2]
            myd['lcal{}'.format(lh)] = food['calories']*i[3]/food['serving_size_g']
            lh+=1
        elif i[1] == '3':
            myd['ssno{}'.format(sn)] = sn
            myd['smeal{}'.format(sn)] = i[2]
            myd['scal{}'.format(sn)] = food['calories']*i[3]/food['serving_size_g']
            sn+=1
        elif i[1] == '4':
            myd['dsno{}'.format(dn)] = dn
            myd['dmeal{}'.format(dn)] = i[2]
            myd['dcal{}'.format(dn)] = food['calories']*i[3]/food['serving_size_g']
            dn+=1
        count+=1
    
    if request.method == 'POST':
        d = request.POST
        query = d['search']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(api_url + query, headers = {'X-Api-Key': 'mHYayv7eKmXcnXbHmeurag==ueCos82ZFg58qgsF'})
        api = json.loads(api_request.content)
        if api == []:
            myd['notvalid'] = 1
            return render(request, 'mealadd.html', myd)
        else:
            new_food = api[0]

            q_all = "select * from meal where uname = '{}'".format(user)
            cursor.execute(q_all)
            meals = cursor.fetchall()

            q2="insert into meal values('{}', '{}', '{}', '{}', '{}', '{}')".format(len(meals)+1, d['meal_name'], d['search'], d['Quantity'], user,  d['mealtime'])
            cursor.execute(q2)
            m.commit()

            if d['meal_name'] == '1':
                myd['bsno{}'.format(count)] = bf
                myd['bmeal{}'.format(count)] = d['search']
                myd['bcal{}'.format(count)] = new_food['calories']*int(d['Quantity'])/new_food['serving_size_g']
                bf+=1
            elif d['meal_name'] == '2':
                myd['lsno{}'.format(count)] = lh
                myd['lmeal{}'.format(count)] = d['search']
                myd['lcal{}'.format(count)] = new_food['calories']*int(d['Quantity'])/new_food['serving_size_g']
                lh+=1
            elif d['meal_name'] == '3':
                myd['ssno{}'.format(count)] = sn
                myd['smeal{}'.format(count)] = d['search']
                myd['scal{}'.format(count)] = new_food['calories']*int(d['Quantity'])/new_food['serving_size_g']
                sn+=1
            elif d['meal_name'] == '4':
                myd['dsno{}'.format(count)] = dn
                myd['dmeal{}'.format(count)] = d['search']
                myd['dcal{}'.format(count)] = new_food['calories']*int(d['Quantity'])/new_food['serving_size_g']
                dn+=1


            myd['cur'] = new_food['name']
            myd['p1'] = new_food['protein_g']*int(d['Quantity'])/new_food['serving_size_g']
            myd['c1'] = new_food['carbohydrates_total_g']*int(d['Quantity'])/new_food['serving_size_g']
            myd['f1'] = new_food['fat_total_g']*int(d['Quantity'])/new_food['serving_size_g']
            myd['s1'] = new_food['sugar_g']*int(d['Quantity'])/new_food['serving_size_g']
            myd['fib1'] = new_food['fiber_g']*int(d['Quantity'])/new_food['serving_size_g']


            return render(request, 'mealadd.html', myd)
        
    return render(request, 'mealadd.html', myd)

def profile(request):
    q_details = """
        select * from user where uname = '{}'
    """.format(user)

    cursor.execute(q_details)
    records = cursor.fetchall()
    details = {}

    for i in records:
        
        try: details['age'] = date.today().year - i[3].year
        except: pass
        try: details['gender'] = i[4]
        except: pass
        try: details['address'] = i[5]
        except: pass
        try: details['email'] = i[11]
        except: pass
        try: details['medical'] = i[7]
        except: pass

    # if request.method == 'POST':
    #      d = request.POST

    #     if 'height' and 'weight' in d.keys():
    #         my = {
    #             'height1': d['height'], 
    #             'weight1': d['weight']
    #             }
    #     return render(request, 'profile.html', my)
    return render(request, 'profile.html', details)

def editprofile(request):
    if request.method == 'POST':
        d = request.POST
        print(d)
        q_check = "Select uname from user where email = '{}'".format(d['email'])
        cursor.execute(q_check)
        records = cursor.fetchall()
        print(records[0][0])
        try:
            if str(records[0][0]) == user or len(records) == 0:
                print('hello')
                q_user = """
                    UPDATE user 
                    SET 
                        dob = '{}',
                        gender = '{}',
                        address = '{}',
                        email = '{}',
                        medical_history = '{}'
                    WHERE
                        uname = '{}';
                """.format(d['dob'], d['gender'], d['address'], d['email'], d['medical'], user)
                cursor.execute(q_user)
                m.commit()
                return render(request, 'profile.html')
        except:
            pass
        return render(request, 'editprofile.html')
    return render(request, 'editprofile.html')

def healthnotes(request):
    cmyd = {}
    if request.method == 'POST':
        d = request.POST
        print(d)
        if 'fetchmeal' in d.keys():
            print(d['fetchmeal'])
            q_meals = "select * from meal where uname = '{}' and CAST(meal_date as date) = '{}'".format(user, d['fetchmeal'])
            cursor.execute(q_meals)
            records = cursor.fetchall()
            
            cmyd = {}
            count = 1
            str_search = ''
            for i in records:
                str_search = str_search + i[2]+ " and "

            query = str_search
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
            api_request = requests.get(api_url + query, headers = {'X-Api-Key': 'mHYayv7eKmXcnXbHmeurag==ueCos82ZFg58qgsF'})
            api = json.loads(api_request.content)

            
            count = 0
            
            bf = 1
            lh = 1
            sn = 1
            dn = 1
            for i in records:
                food = api[count]
                
                if i[1] == '1':
                    
                    cmyd['bsno{}'.format(bf)] = bf
                    cmyd['bmeal{}'.format(bf)] = i[2]
                    cmyd['bcal{}'.format(bf)] = food['calories']*i[3]/food['serving_size_g']
                    bf+=1
                elif i[1] == '2':
                    cmyd['lsno{}'.format(lh)] = lh
                    cmyd['lmeal{}'.format(lh)] = i[2]
                    cmyd['lcal{}'.format(lh)] = food['calories']*i[3]/food['serving_size_g']
                    lh+=1
                elif i[1] == '3':
                    cmyd['ssno{}'.format(sn)] = sn
                    cmyd['smeal{}'.format(sn)] = i[2]
                    cmyd['scal{}'.format(sn)] = food['calories']*i[3]/food['serving_size_g']
                    sn+=1
                elif i[1] == '4':
                    cmyd['dsno{}'.format(dn)] = dn
                    cmyd['dmeal{}'.format(dn)] = i[2]
                    cmyd['dcal{}'.format(dn)] = food['calories']*i[3]/food['serving_size_g']
                    dn+=1
                count+=1
        
            q_notes = """
                select * from healthnote
                where
                    note_day = '{}' and uname = '{}'
            """.format( d['fetchmeal'], user)

            cursor.execute(q_notes)
            records = cursor.fetchall()

            for i in records:
                cmyd['notedate1'] = d['fetchmeal']
                cmyd['notetext1'] = i[1]
                if i[3] == '1':
                    cmyd['note_color1'] = '#e44c65'
                elif i[3] == '2':
                    cmyd['note_color1'] = '#5dba7d'
                elif i[3] == '3':
                    cmyd['note_color1'] = '#f2e758'
        
        if 'notetoday' in d.keys():
            q_fetch = "select * from healthnote where note_day = '{}'".format(date.today())
            cursor.execute(q_fetch)
            records = cursor.fetchall()
            if len(records) != 0:
                q_up = """
                    UPDATE healthnote 
                    SET 
                        note = '{}',
                        color = '{}'
                    WHERE
                        uname = '{}'
                """.format(d['notetoday'], d['category'], user)
                cursor.execute(q_up)
                m.commit()
            else:
                
                q_insert = """
                    insert into healthnote
                    values
                        ("{}", '{}', '{}', '{}')
                """.format(date.today(), d['notetoday'], user, d['category'])
                cursor.execute(q_insert)
                m.commit()
                cmyd['noteadded'] = 1
            
        return render(request, 'healthnotes.html', cmyd)
    return render(request, 'healthnotes.html')

def customrecipes(request):
    if request.method == 'POST':
        d = request.POST
        send_d = {}
        print(d)
        q_search = """
            select * from nutrition
            where 
                food_name = '{}'
        """.format(d['foodname'])
        cursor.execute(q_search)
        records = cursor.fetchall()
        if len(records) != 0:
            send_d['exist'] = 1
        else:
            try:
                if bool(d['sodium'])==False and bool(d['potassium'])==False and bool(d['cholesterol'])==False and bool(d['fat_sat'])==False and bool(d['fiber'])==False and bool(d['sugar'])==False:
                    print('hello')
                    q_insert = """
                        insert into nutrition
                        values
                            ('{}', '{}', '{}', '{}', NULL, NULL, NULL, '{}', NULL, '{}', NULL, NULL)    
                    """.format(d['foodname'], d['calories'], d['serving'], d['protein'], d['carbohydrates'], d['fat'])
                    cursor.execute(q_insert)
                    m.commit()
                    send_d['added'] = 1
                else:
                    print('hello2')
                    try:
                        q_insert = """
                            insert into nutrition
                            values
                                ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')    
                        """.format(d['foodname'], d['calories'], d['serving'], d['protein'], d['sodium'], d['potassium'], d['cholesterol'], d['carbohydrates'], d['fat_sat'], d['fat'], d['fiber'], d['sugar'])
                        cursor.execute(q_insert)
                        m.commit()
                        send_d['added'] = 1
                    except:
                        send_d['notvalid'] = 1
                        pass
            except:
                send_d['notvalid'] = 1
                pass
        return render(request, 'customrecipes.html', send_d)
    return render(request, 'customrecipes.html')

def login(request):
    try:
        if request.method == 'POST':
            m=my.connect(host="localhost",user="root",passwd="Sai_dbms",database="caltrack")
            cursor=m.cursor()
            d = request.POST
            q1="Select uname, pass from user where uname='{}'".format(d['username'])
            cursor.execute(q1)
            records = cursor.fetchall()
            if len(records) != 0:
                i = records[0]
                if str(i[1]) == d['password']:
                    print("hello")
                    global user 
                    user = d['username']
                    return home(request)
    except:
        pass
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        m=my.connect(host="localhost",user="root",passwd="Sai_dbms",database="caltrack")
        cursor=m.cursor()
        d = request.POST
        print(d)
        q1="Select uname from user where uname='{}'".format(d['username'])
        cursor.execute(q1)
        records = cursor.fetchall()
        print(records)
        if len(records) != 0:
            d = {'invalid': 1}
            return render(request, 'signup.html', d)
        if len(records) == 0:
            print(date.today())
            q2="insert into user values('{}', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{}', '{}', '{}')".format(d['username'], d['password'], date.today(), d['email'])
            cursor.execute(q2)
            m.commit()
    return render(request, 'signup.html')

