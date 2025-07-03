import google.generativeai as genai
genai.configure(api_key="AIzaSyBrbvuOGmyAsrR3c2T6zRL-Q7EN85tEvHQ")

models = genai.list_models()
for model in models:
    print(model.name)
