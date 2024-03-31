from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import User, Contact, Appointment
from django.contrib import messages
from twilio.rest import Client
import random
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import os
import re

# Create your views here.
def landing(request):
    return render(request,'food/landing.html')

def home(request):
    global user_mobile
    global user_name
    try:
        if str(user_mobile) in request.session:
            return render(request, 'food/home.html',{'user_name':user_name})
        else:
            messages.warning(request,'Login First')
            return HttpResponseRedirect('/login')
    except NameError as e:
        messages.warning(request,'Login First')
        return HttpResponseRedirect('/login')

def about(request):
    global user_mobile
    global user_name
    try:
        if str(user_mobile) in request.session:
            return render(request, 'food/about.html',{'user_name':user_name})
        else:
            user_name=''
            return render(request, 'food/about.html',{'user_name':user_name})
    except NameError as e:
        user_name=''
        return render(request, 'food/about.html',{'user_name':user_name})

def services(request):
    global user_mobile
    global user_name
    try:
        if str(user_mobile) in request.session:
            return render(request, 'food/services.html',{'user_name':user_name})
        else:
            user_name=''
            return render(request, 'food/services.html',{'user_name':user_name})
    except NameError as e:
        user_name=''
        return render(request, 'food/services.html',{'user_name':user_name})

def contact(request):
    global user_mobile
    global user_name
    try:
        if str(user_mobile) in request.session:
            return render(request, 'food/contact.html',{'user_name':user_name})
        else:
            user_name=''
            return render(request, 'food/contact.html',{'user_name':user_name})
    except NameError as e:
        user_name=''
        return render(request, 'food/contact.html',{'user_name':user_name})

def signup(request):
    if request.method=='POST':
        users=User.objects.all()
        global user_name
        global user_email
        global user_mobile
        user_name=request.POST.get('name')
        user_email=request.POST.get('email')
        user_mobile=request.POST.get('mobile')
        if len(str(user_mobile))!=10:
            messages.error(request,'Enter a valid mobile number')
            return HttpResponseRedirect('/signup')
        for user in users:
            if user_mobile==str(user.mobile):
                messages.warning(request,'This mobile is already registered.')
                return HttpResponseRedirect('/signup')
    
        request.session[str(user_name)]=user_name
        request.session[str(user_email)]=user_email
        request.session[str(user_mobile)]=user_mobile
        request.session.set_expiry(0)
        return redirect('signup_otp')
    else:
        return render(request,'food/signup.html') 


def signup_otp(request):
    global user_name
    global user_email
    global user_mobile
    global otp
    if request.method=='POST':
        otp_code = request.POST.get('signup_otp')
        if str(otp) == otp_code:
            print(True)
            user_name=request.session[str(user_name)]
            user_email=request.session[str(user_email)]
            user_mobile=request.session[str(user_mobile)]
            user=User(name=user_name,email=user_email,mobile=user_mobile)
            user.save()
            messages.success(request,'Verified Successfully')
            return HttpResponseRedirect('/home')
        else:
            messages.warning(request,'Enter valid OTP')
            return HttpResponseRedirect('/signup_otp')
    else:
        if str(user_mobile) in request.session:
            mobile=request.session[str(user_mobile)]
            verified_number = "+91"+str(mobile)
            otp=random.randint(100000,999999)
            account_sid="AC8b2868ffb82672e1a4a89496bbdc9435"
            auth_token="bf5c378416ba3d267aa63a8b312733c9"
            client=Client(account_sid,auth_token)
            msg=client.messages.create(
                    body = f"Your otp is: {otp}",
                    from_ = "+13252406647",
                    to = verified_number
                )
            return render(request,'food/signup_otp.html')
        else:
            messages.warning(request,'Login First')
            return HttpResponseRedirect('/login')


def login(request):
    if request.method=='POST':
        users=User.objects.all()
        global user_mobile
        global user_name
        user_mobile=request.POST.get('mobile')
        for user in users:
            if user_mobile == str(user.mobile):
                user_name=user.name
                request.session[str(user_mobile)]=user_mobile
                request.session[str(user_name)]=user_name
                request.session.set_expiry(0)
                return HttpResponseRedirect('/login_otp')
            else:
                pass
        messages.warning(request,"You don't have an account. Register Here!")
        return HttpResponseRedirect('/signup')
    else:
        return render(request,'food/login.html') 


def login_otp(request):
    global user_mobile
    global otp
    if request.method=='POST':
        otp_code = request.POST.get('login_otp')
        if otp_code == str(otp):
            messages.success(request,'Logged in Successfully')
            return HttpResponseRedirect('/home')
    else:
        if str(user_mobile) in request.session:
            mobile=request.session[str(user_mobile)]
            verified_number = "+91"+str(mobile)
            otp=random.randint(100000,999999)
            account_sid="AC8b2868ffb82672e1a4a89496bbdc9435"
            auth_token="bf5c378416ba3d267aa63a8b312733c9"
            client=Client(account_sid,auth_token)
            msg=client.messages.create(
                body = f"Your otp is: {otp}",
                from_ = "+13252406647",
                to = verified_number
                )
            return render(request,'food/login_otp.html')
        else:
            messages.warning(request,'Login First')
            return HttpResponseRedirect('/login')


def inputs(request):
    global user_mobile
    global user_name
    try:
        if str(user_mobile) in request.session:
            if request.method=='POST':
                age=request.POST.get('age')
                height=request.POST.get('height')
                weight=request.POST.get('weight')
                gender=request.POST.get('gender')
                region=request.POST.get('region')
                diseases=request.POST.get('diseases')
                allergies=request.POST.get('allergies')
                diet=request.POST.get('diet')
                recommended=recommend(age,gender,weight,height,diet,diseases,region,allergies)
                return render(request,'food/output.html',{'data':recommended})
            else:
                return render(request,'food/inputs.html')
        else:
            messages.warning(request,'Login First')
            return HttpResponseRedirect('/login')
    except NameError as e:
        messages.warning(request,'Login First')
        return HttpResponseRedirect('/login')
            


def report(request):
    global user_mobile
    global user_name
    try:
        if str(user_mobile) in request.session:
            if request.method == 'POST':
        
                uploaded_file = request.FILES.get('fileInput')
                print(uploaded_file)
                recommends=health("C:/Users/ps200/Music/optieats/food/templates/food/Laboratory-Blood-Test-Results.png")
                return render(request,'food/output.html',{'recommends':recommends})
            else:
                return render(request,'food/report.html')
        else:
            messages.warning(request,'Login First')
            return HttpResponseRedirect('/login')
    except NameError as e:
        messages.warning(request,'Login First')
        return HttpResponseRedirect('/login')

def appointment(request):
    global user_mobile
    global user_name
    try:
        if str(user_mobile) in request.session:
            if request.method == 'POST':
                selected_hospital=request.POST.get('hospital')
                selected_doctor=request.POST.get('doctor')
                selected_date=request.POST.get('date')
                selected_time=request.POST.get('time')
                appointment=Appointment(hospital=selected_hospital, doctor=selected_doctor, date=selected_date, time=selected_time)
                appointment.save()
                message = "Appointment scheduled successfully!"
                return render(request,'food/appointment.html',{'message':message})
            else:
                return render(request,'food/appointment.html')
        else:
            messages.warning(request,'Login First')
            return HttpResponseRedirect('/login')
    except NameError as e:
        messages.warning(request,'Login First')
        return HttpResponseRedirect('/login')

def recommend(age,gender,weight,height,veg_or_nonveg,disease,region,allergies):
  os.environ["OPENAI_API_KEY"] = "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"

  llm_resto = OpenAI(temperature=0.5,model='gpt-3.5-turbo-instruct')

  my_prompt = PromptTemplate(
    input_variables=["age","gender","weight","height","veg_or_nonveg","disease","region","allergies"],
    template="Diet Recommendation System\n"
             "I want you to recommend  breakfast, lunch, dinner with nutritional value count of the recommended food and also suggest a workout "
             "based on the following creitria\n"
             "Person age : {age}\n"
             "Person gender : {gender}\n"
             "Person weight : {weight}\n"
             "Person height : {height}\n"
             "Person veg_or_nonveg : {veg_or_nonveg}\n"
             "Person disease : {disease}\n"
             "Person region : {region}\n"
             "Person allergies : {allergies}."

  )

  chain_new = LLMChain(llm=llm_resto,prompt=my_prompt)

  input_data = {
    'age' : age,
    'gender' : gender,
    'weight' : weight,
    'height' : height,
    'veg_or_nonveg' : veg_or_nonveg,
    'disease' : disease,
    'region' : region,   'allergies' : allergies
  }

  results = chain_new.run(input_data)

  print(results)

  breakfast = re.findall(r"Breakfast:(.*?)Lunch:",results,re.DOTALL)
  lunch = re.findall(r"Lunch:(.*?)Dinner:",results,re.DOTALL)
  dinner = re.findall(r"Dinner:(.*?)Workout:",results,re.DOTALL)
  workout = re.findall(r'Workout:(.*?)$', results, re.DOTALL)

  # Breakfast Recommender
  breakfast_str = breakfast
  # Convert list to string
  breakfast_string = ', '.join(breakfast_str)

  #print(breakfast_string)

  # Split the string by '\n-' to separate each meal
  breakfast_list = breakfast_string.split('\n-')

  # Remove any empty strings and strip whitespace from each element
  breakfast_list = [meal.strip() for meal in breakfast_list if meal.strip()]

  #print(breakfast_list)





  #print(breakfast_list)

  # lunch Recommender
  lunch_str = lunch

  # Convert list to string
  lunch_string = ', '.join(lunch_str)

  #print(lunch_string)

  # Split the string by '\n-' to separate each meal
  lunch_list = lunch_string.split('\n-')

  # Remove any empty strings and strip whitespace from each element
  lunch_list = [meal.strip() for meal in lunch_list if meal.strip()]

  #print(lunch_list)

  # Dinner Recommender
  dinner_str = dinner
  # Convert list to string
  dinner_string = ', '.join(dinner_str)

  #print(dinner_string)

  # Split the string by '\n-' to separate each meal
  dinner_list = lunch_string.split('\n-')

  # Remove any empty strings and strip whitespace from each element
  dinner_list = [meal.strip() for meal in dinner_list if meal.strip()]

  #print(dinner_list)

  # Workout Recommender
  workout_str = workout
  # Convert list to string
  workout_string = ', '.join(workout_str)

 #print(workout_string)

  # Split the string by '\n-' to separate each meal
  workout_list = workout_string.split('\n-')

  # Remove any empty strings and strip whitespace from each element
  workout_list = [meal.strip() for meal in workout_list if meal.strip()]

 #print(workout_list)

  # If workout is not work out

  if workout==[]:
    workout_list = ['- Low-impact exercises such as walking, swimming, or cycling for 30 minutes, 5 times a week.',
             '- Yoga or stretching exercises to improve flexibility and reduce stress.']
  else:
    workout_list = []
    workout_str = workout

    # Convert list to string
    workout_string = ', '.join(workout_str)

    # Split the string by '\n-' to separate each meal
    workout_list = workout_string.split('\n-')

    # Remove any empty strings and strip whitespace from each element
    workout_list = [meal.strip() for meal in workout_list if meal.strip()]

    #print(workout_list)


  # Returning the results

  return breakfast_list


def health(image_path):
  
  import os
  os.environ["OPENAI_API_KEY"] = "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"


  from langchain.prompts import PromptTemplate
  from langchain.llms import OpenAI
  from langchain.chains import LLMChain
  
  # OCR

  import cv2
  import pytesseract
  import matplotlib.pyplot as plt
  from IPython.display import Image
  import numpy as np
  from pprint import pprint
  from pytesseract import Output

  file = image_path

  img = cv2.imread(file)

  text = pytesseract.image_to_string(img)

  data_string = '''Component Your Value StandardRange Units Flag\n\n \n\nWhite Blood Cell Count 5.4 4.0- 11.0 K/ut\nRed Blood Cell Count 5.20 4.40 - 6.00 M/uL.\nHemoglobin 16.0 13.5 - 18.0 g/d\nHematocrit 47.2 40.0 - 52.0 %\n\nMev 91 80 - 100 fl\n\nMcH 30.8 27.0 - 33.0 Pg\n\nMcHc 33.9 31.0 - 36.0 g/d\nRDW 12.7 <16.4 - %\nPlatelet Count 149 150 - 400 KL.\nDifferential Type ‘Automated\n\nNeutrophil % 56 49.0 - 74.0 %\nLymphocyte % 23 26.0 - 46.0 %\nMonocyte % 13 2.0 - 12.0 %\nEosinophil % zi 0.0 - 5.0 %\nBasophil % 1 0.0 - 2.0 %\n\n‘Abs. Neutrophil 34 2.0 - 8.0 Kyu\n‘Abs. Lymphocyte 12 1.0- 5.1 Kut\n‘Abs. Monocyte 0.7 0.0 - 0.8 Kyu\n‘Abs. Eosinophil 0.4 0.0- 0.5 Kyu\n\nAbs. Basophil 0.0 0.0 - 0.2 K/ut,\n\x0c'''

  data_list = text.split("\n")
  data_dict = {}

  for line in data_list:
      if line.strip():  # To skip empty lines
          components = line.split()
          key = " ".join(components[:-4])  # Component name
          value = " ".join(components[-4:])  # Value, StandardRange, Units, Flag
          data_dict[key] = value


  # Split the text by newline characters to separate each line
  lines = text.split("\n")

  # Initialize an empty dictionary to store key-value pairs
  data_dict = {}

  # Iterate over each line in the lines list
  for line in lines:
      # Skip empty lines
      if line.strip():
          # Split each line by whitespace
          components = line.split()
          # Join the first three components as the key
          key = " ".join(components[:2])
          # Join the rest of the components as the value
          value = " ".join(components[2:])
          # Add the key-value pair to the dictionary
          data_dict[key] = value

  wbc = data_dict['WBCs (billion/L)'][0]
  neutrophils = data_dict['Neutrophils (%)'][0]
  hemoglobin = data_dict['Hb (g/dL)'][0]
  platelets = data_dict['Platelets (billion/L)'][0]
  rbc = data_dict['RBCs (trillion/L)'][0]

    # Original dictionary
  #data = {'blood lest': 'Result Normal Value', 'WBCs (billion/L)': '8.00 3.5 to 10.5'}

  # Create a list of keys to iterate over
  #keys_to_modify = [key for key in data_dict.keys() if 'WBC (billion/L)' in key]

  # Iterate over the list of keys
  #for key in keys_to_modify:
      # Replace "WBC" with "Normal WBC" in the key
      #new_key = key.replace('WBC (billion/L)', 'WBC')
      # Update the dictionary with the new key and the corresponding value
      #data_dict[new_key] = data_dict.pop(key)

  llm_resto = OpenAI(temperature=0,model='gpt-3.5-turbo-instruct')

  my_prompt = PromptTemplate(
    input_variables=["wbc","rbc","platelets","neutrophils","hemoglobin"],
    template="Diet Recommendation System\n"
            "I want you to find what diseases the user is suffering from the user input based on medical aspect "
            "based on the following creitria\n"
            "Person white blood cell : {wbc}\n"
            "Person red blood cell : {rbc}\n"
            "Person platelets : {platelets}\n"
            "Person neutrophils : {neutrophils}\n"
            "Person hemoglobin : {hemoglobin}\n"
  )

  chain_new = LLMChain(llm=llm_resto,prompt=my_prompt)
  input_data = {'wbc' : wbc,
                'rbc' : rbc,
                'platelets' : platelets,
                'neutrophils' : neutrophils,
                'hemoglobin' : hemoglobin}



  results = chain_new.run(input_data)
  return results