from fastapi import FastAPI, Depends, HTTPException, Query, status , Body , Header
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import PIL
import google.generativeai as genai
from fastapi import FastAPI, Body
from pydantic import BaseModel
import requests 
from io import BytesIO
from groq import Groq
from openai import OpenAI

client = OpenAI(api_key=("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"))

app : FastAPI = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_AI_STUDIO = "AIzaSyAK6vhyL_4BvSlHZgY3YjSTVePzU5ZiIUM"
genai.configure(api_key=GOOGLE_AI_STUDIO)
model = genai.GenerativeModel('gemini-pro-vision')
model1 = genai.GenerativeModel(model_name="gemini-1.0-pro")


def load_image_from_url(image_url):
    response = requests.get(image_url)
    image = PIL.Image.open(BytesIO(response.content))
    return image

class CheckBanner(BaseModel):
    image_url: str | None = None
    
    
def check_banner(image_data : CheckBanner = Body(...)) -> str :
    Profile1 = load_image_from_url('https://res.cloudinary.com/dfkn6xcg4/image/upload/v1709367740/1704587928601_t90lck.jpg')
    Profile2 = load_image_from_url('https://res.cloudinary.com/dfkn6xcg4/image/upload/v1709367740/1708819917247_xur0my.jpg')
    Profile3 = load_image_from_url(image_data.image_url)
    
    primary_images = [Profile1, Profile2, Profile3]

    response = model.generate_content([
        "Effectively analyze the primary banners of top creators on LinkedIn and offer comprehensive ratings, tips, suggestions, and content insights, follow these steps. These are the two primary banners",
        primary_images[0],
        primary_images[1],
        "individually assess each primary banner, considering factors like design, content quality, and overall attractiveness to viewers. Assign a rating out of 10 to each banner based on its effectiveness in capturing attention and conveying the desired message. Provide actionable tips and suggestions for improving each banner, including adjustments to design elements, content refinement, and other enhancements. Utilize tools such as a generative model to analyze the banners thoroughly and generate detailed insights into their strengths and areas for improvement. Present the analysis and recommendations in a clear and organized manner, possibly using Markdown formatting for readability. Tailor the assessment to align with the banners' overarching goals, whether it's showcasing skills, attracting clients, or promoting a personal brand.",
        "This is secondary banner",
        primary_images[2],
        "Only give suggestions, tips, and rating of the secondary banner. Primary banners are only for taking advice"
    ])

    return response.text     
    

class HeadlineRequest(BaseModel):
    prev_headline: str

def headline_check(feild : str = Query(None) , subfeild : str = Query(None) ,  Prev_headline : HeadlineRequest = Body(...) ) -> str :
    if feild and subfeild :
        client = Groq(api_key='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')
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You are an Expert in Writing Headlines for linkedin profile "
                },
                {
                    "role": "user",
                    "content": f"""The user is  {feild} and expert in {subfeild} . His  headline is ***{Prev_headline}*** . !!!You have to improve this headline in a very professional and apealing way and in refernce to the  headline!!! . Dont give anything more just the improved version of the headline"""
                },
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        return(completion.choices[0].message.content)
    else :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "invalid feild")
    


def check_token(xtts_token : str = Header(...)) -> bool :
    if xtts_token == 'Abdulhadi123456789' :
        return True
    else :
        return False

def load_image_from_url(image_url):
    response = requests.get(image_url)
    image = PIL.Image.open(BytesIO(response.content))
    return image


class CheckProfile(BaseModel):
    image_url: str | None = None

# Function to check profile
def check_profile(image_data: CheckProfile = Body(...)) -> str:
    Profile1 = load_image_from_url('https://res.cloudinary.com/dfkn6xcg4/image/upload/v1709453195/3_rarjnr.jpg')
    Profile2 = load_image_from_url('https://res.cloudinary.com/dfkn6xcg4/image/upload/v1709453196/2_mj13hg.jpg')
    Profile3 = load_image_from_url(image_data.image_url)
    
    primary_images = [Profile1, Profile2, Profile3]

    # Generate content using the model
    response = model.generate_content([
        "The below primary images are profile pictures of the best creators in the LinkedIn community. These profiles are 9/10",
        primary_images[0], primary_images[1],
        "This is the secondary image. You have to give suggestions and tips on how this profile image can be improved. Also give rating out of 10",
        primary_images[2]
    ])
    return response.text

def check_resume(resume : str = Body(...)) -> str :


    convo = model1.start_chat(history=[
  {
    "role": "user",
    "parts": ["You are an expert in resume making . Below are the points you have to follow while making resume .1) Quantify impact (Numbers in bullet points eg . '30%' sales increased and etc)2) No Repeatation of words3) You should remove weak action verbs from your resume.4) you can use both the present and/or past tense to describe your current job. However, you should always use the past tense when describing your previous experiences and achievements.5) Avoided Responsibility-oriented Words. Your resume should focus on your accomplishments, not your responsibilities6) Avoid Spelling mistakes7) Top student resumes are between 450 and 650 words long.8) Avoid using paragraphs. Use bullet points instead.9) You should have 12 bullets points altogether in your project section10) Each of your bullet points should be between 10 and 30 words long11) Even if your bullet point is within that range, remember that it should not exceed two lines on your resume (visually).12) Remove superfluous words that take up space and add little value eg.   Before : Carried out evaluations of various strategies in order to save clients $200k in fixed costs...After (Fillers removed) : Evaluated 15+ strategies to save clients $200k in fixed costs...13) Remove vague buzzwords which add little value eg .passionate , dynamic14) No unnecessary business jargon eg.BEFORE: WITH BUZZWORDS• Highly motivated individual with strong leadership and management skills, with extensive experience managing cross-functional teamsAFTER: NO BUZZWORDS• Managed a 5-member cross-functional (product, engineering, sales, support) team and coordinated with six business partners toward the successful launch of an e-commerce platform.15) Make sure your dates are formatted correctly eg . feburary 2020 - Till Date , December 2021 - October 20232016-2017 (just years), You should be consistent with your date formats.16) In terms of personal details, your resume should contain your name, location, and key contact details (e.g. your email). You should avoid adding in other personal details, like date of birth, gender or nationality. Let's look at a few personal detail checks.17) A good filename looks like Jane-Smith-Resume.pdf or Jane-Smith-Resume.docx.18) Remove any personal pronouns from your resume eg.BeforeI managed a 5-member cross-functional (product, engineering, sales, support) team and we coordinated with my company's six business partners toward the successful launch of our e-commerce platform.AfterManaged a 5-member cross-functional (product, engineering, sales, support) team and coordinated with six business partners toward the successful launch of an e-commerce platform.19) Make sure you avoid the passive voice in your bullet points20) Ensure your bullet points are consistent in punctuation and formatting.21) Summary are only appropriate for mid- to senior-level applicants, or career changers, but not entry-level applicants.22) Get your education section in shape, plus see proven examples23) A skills section is a short, optional resume section that can be used to include technical and hard skills that you have, especially if you haven’t been able to include them elsewhere in your resume.24) Communication , Employers want someone that can clearly communicate with anyone the job requires them to - whether that is a key stakeholder, team member or client.You should add more examples of communication skills on your resume.25) Leadership ,Employers want to know if you can own a project, manage a team and take responsibility .Involve evidence of leadership.26) Analytical and Problem-solving ,Analytical skills refer to your ability to break down complex problems, evaluate them effectively, and come up with appropriate solutions.27) Teamwork , Employers want to know if you can work effectively with others to achieve common goals .Involve evidence of teamwork.28) Drive and Initiative ,Employees who show strong initiative are characterized by their proactivity, self-starting nature and persistence in solving difficult problems. Not enough drive and initiative demonstrated.29) Dont use embedded link . Use full link as string if neccesaryyou have to make sure all these points are folllowed . Remeber these are complusory keypoints in making a ats optimized resume . If you find anything against it you have to correct it and rewrite all the resume from start . Below is the resume . Analyze it and improve if nessasry."]
  },
  {
    "role": "model",
    "parts": ["## Resume Analysis and Improvement Process\n\nI'm ready to analyze the resume you provide and improve it based on the 29 key points you've outlined. Please share the resume content, and I'll carefully review it, making necessary adjustments to optimize it for ATS systems and ensure it effectively showcases the candidate's skills and experiences. \n\n**Here's how I'll approach the analysis and improvement:**\n\n1. **Quantifiable Impact:** I'll ensure each bullet point includes quantifiable metrics to demonstrate the impact of the candidate's actions. \n2. **Word Repetition:** I'll eliminate repetitive words and phrases to maintain conciseness and variety.\n3. **Action Verbs:** Weak action verbs will be replaced with strong, impactful alternatives that highlight achievements.\n4. **Tense Consistency:** I'll ensure past tense is used for previous experiences and present tense for the current role.\n5. **Accomplishment Focus:** The resume will be revised to emphasize accomplishments rather than responsibilities.\n6. **Spelling and Grammar:** Thorough proofreading will eliminate any spelling or grammatical errors.\n7. **Word Count:** The resume length will be adjusted to fall within the optimal range of 450-650 words.\n8. **Bullet Points:** Paragraphs will be converted into concise bullet points for improved readability. \n9. **Project Section Length:** The project section will be reviewed to ensure it contains approximately 12 bullet points.\n10. **Bullet Point Length:** Each bullet point will be edited to adhere to the 10-30 word range and two-line visual limit.\n11. **Filler Words:** Superfluous words will be removed to maintain a concise and impactful writing style.\n12. **Buzzwords:** Vague buzzwords like \"passionate\" or \"dynamic\" will be eliminated.\n13. **Business Jargon:** Unnecessary business jargon will be replaced with clear and concise language.\n14. **Date Formatting:** Dates will be formatted consistently throughout the resume. \n15. **Personal Details:** The resume will only include essential personal details, such as name,"]
  },
  {
    "role": "user",
    "parts": ["You are an expert in resume making . Below are the points you have to follow while making resume .1) Quantify impact (Numbers in bullet points eg . '30%' sales increased and etc)2) No Repeatation of words3) You should remove weak action verbs from your resume.4) you can use both the present and/or past tense to describe your current job. However, you should always use the past tense when describing your previous experiences and achievements.5) Avoided Responsibility-oriented Words. Your resume should focus on your accomplishments, not your responsibilities6) Avoid Spelling mistakes7) Top student resumes are between 450 and 650 words long.8) Avoid using paragraphs. Use bullet points instead.9) You should have 12 bullets points altogether in your project section10) Each of your bullet points should be between 10 and 30 words long11) Even if your bullet point is within that range, remember that it should not exceed two lines on your resume (visually).12) Remove superfluous words that take up space and add little value eg.   Before : Carried out evaluations of various strategies in order to save clients $200k in fixed costs...After (Fillers removed) : Evaluated 15+ strategies to save clients $200k in fixed costs...13) Remove vague buzzwords which add little value eg .passionate , dynamic14) No unnecessary business jargon eg.BEFORE: WITH BUZZWORDS• Highly motivated individual with strong leadership and management skills, with extensive experience managing cross-functional teamsAFTER: NO BUZZWORDS• Managed a 5-member cross-functional (product, engineering, sales, support) team and coordinated with six business partners toward the successful launch of an e-commerce platform.15) Make sure your dates are formatted correctly eg . feburary 2020 - Till Date , December 2021 - October 20232016-2017 (just years), You should be consistent with your date formats.16) In terms of personal details, your resume should contain your name, location, and key contact details (e.g. your email). You should avoid adding in other personal details, like date of birth, gender or nationality. Let's look at a few personal detail checks.17) A good filename looks like Jane-Smith-Resume.pdf or Jane-Smith-Resume.docx.18) Remove any personal pronouns from your resume eg.BeforeI managed a 5-member cross-functional (product, engineering, sales, support) team and we coordinated with my company's six business partners toward the successful launch of our e-commerce platform.AfterManaged a 5-member cross-functional (product, engineering, sales, support) team and coordinated with six business partners toward the successful launch of an e-commerce platform.19) Make sure you avoid the passive voice in your bullet points20) Ensure your bullet points are consistent in punctuation and formatting.21) Summary are only appropriate for mid- to senior-level applicants, or career changers, but not entry-level applicants.22) Get your education section in shape, plus see proven examples23) A skills section is a short, optional resume section that can be used to include technical and hard skills that you have, especially if you haven’t been able to include them elsewhere in your resume.24) Communication , Employers want someone that can clearly communicate with anyone the job requires them to - whether that is a key stakeholder, team member or client.You should add more examples of communication skills on your resume.25) Leadership ,Employers want to know if you can own a project, manage a team and take responsibility .Involve evidence of leadership.26) Analytical and Problem-solving ,Analytical skills refer to your ability to break down complex problems, evaluate them effectively, and come up with appropriate solutions.27) Teamwork , Employers want to know if you can work effectively with others to achieve common goals .Involve evidence of teamwork.28) Drive and Initiative ,Employees who show strong initiative are characterized by their proactivity, self-starting nature and persistence in solving difficult problems. Not enough drive and initiative demonstrated.29) Dont use embedded link . Use full link as string if neccesaryyou have to make sure all these points are folllowed . Remeber these are complusory keypoints in making a ats optimized resume . If you find anything against it you have to correct it and rewrite all the resume from start . Below is the resume . Analyze it and improve if nessasry.\n\nAbdul Hadi\nKarachi, Sindh, Pakistan ah912425@gmail.com 03120202881 in/abdul-hadi-28a46221b/ https://www.abdulhadi.info/\nEXPERIENCE\nFRONT-END DEVELOPER\nBrilliant IT Solution April 2022 - January 2024, Karachi , PK\n• Functioned as a frontend developer within a 10-member team, contributing to a high-load project with Next.js.\n• Implement React Framework for interactive interfaces, ensuring seamless data updates.\n• Employed Next.js for server-side rendering, boosting performance by 30% to manage high traffic.\nDirected the utilization of generative AI algorithms to revamp project functionalities, contributing to a 50% reduction in manual tasks and a\n15% boost in overall project performance metrics.\n•\n• Developed frontend solutions, ensuring compatibility across devices and browsers.\n• Optimized user experience through efficient code architecture and responsive design principles.\nPROJECTS\nPORTFOLIO\nPersonal • https://www.abdulhadi.info/\n• Engineered a modern portfolio using Next.js, Tailwind CSS, and Sanity CMS, showcasing expertise in web development technologies.\n• Distinguished the portfolio with an AI-generated chatbot powered by OpenAI, offering interactive interaction for visitors.\n• Engineered a seamless integration of Nextjs frontend , resulting in a 40% reduction in loading time and 25% increase in user retention rate .\nINTELLIVERSE\nINTELLIVERSE • https://sass-mu-six.vercel.app/\nDirected the creation of an advanced SaaS platform catering to professionals and students, utilizing AI to optimize LinkedIn profiles; drove a\n45% rise in user acquisition and a 20% increase in user satisfaction levels quarterly.\n•\n• Boosted user engagement by 40% through AI-driven features for job seekers and recruiters.\n• Streamlined ATS optimization tools, resulting in a 30% increase in resume visibility.\n• Enabled seamless LinkedIn post creation, facilitating effortless sharing of professional content.\n• Ensured robust backend in python, reducing downtime by 20% and enhancing scalability.\n• Led cross-functional teams, resulting in a 25% improvement in project delivery time.\nPAINTIFY\nA & H Enterprise • https://nextjs-commerce-azure-chi.vercel.app/ • June 2023 - August 2023\n• Initiated an innovative e-commerce platform with generative AI customer service, boosting user engagement by 40%.\n• Integrated Shopify as the backend platform, ensuring scalability and robustness for product management and secure transactions.\nAssessed a visually appealing and intuitive frontend design powered by Next.js and Tailwind CSS, resulting in a 25% reduction in user\nonboarding time and a 20% increase in retention rates, contributing to a 15% growth in monthly recurring revenue.\n•\nEnhanced loading speed by 30% through code optimization and image compression techniques, resulting in a significant decrease in bounce\nrates and a 20% rise in search engine rankings.\n•\nEDUCATION\nBachelors in Computer Science\nFAST NUCES KARACHI • Karachi , PK • 2025\nSKILLS\nProgramming Languages: C++ , C , Python , Javascript\nFrameworks and Libraries: FastAPI , ReactJS , Next.js , Framer Motion , Tailwind CSS\nDatabases: SQL (Structured Query Language) , PostgreSQL\nDevelopment Tools: Docker , Git\nE-commerce Platforms: Headless Shopify\nContent Management Systems (CMS): Sanity\nAI and Machine Learning: Generative A"]
  },
  {
    "role": "model",
    "parts": ["**Resume Analysis and Improvement**\n\n**Abdul Hadi**\nKarachi, Sindh, Pakistan\nah912425@gmail.com\n03120202881\nin/abdul-hadi-28a46221b/\nhttps://www.abdulhadi.info/\n\n**Summary**\nFront-end developer with 2+ years of experience in building and maintaining high-traffic web applications. Proven ability to use React, Next.js, and Generative AI to develop innovative and engaging user experiences.\n\n**Experience**\n\n**Front-end Developer**\nBrilliant IT Solution, Karachi, PK\nApril 2022 - January 2024\n\n* Developed frontend for a high-load project using Next.js, achieving a 30% performance boost in managing high traffic\n* Employed Generative AI algorithms to revamp project functionalities, reducing manual tasks by 50% and boosting performance metrics by 15%\n* Built responsive and device-compatible frontend solutions\n* Optimized user experience through efficient code architecture and design principles\n\n**Projects**\n\n**Portfolio**\n* Built a personal portfolio using Next.js, Tailwind CSS, and Sanity CMS, showcasing web development expertise\n* Integrated an AI-powered chatbot using OpenAI to enhance user engagement\n* Reduced loading time by 40% and increased user retention rate by 25% through Next.js frontend integration\n\n**Intelliverse**\n* Led the development of a SaaS platform for professionals and students using AI to optimize LinkedIn profiles\n* Increased user acquisition by 45% and satisfaction by 20% through AI-driven features\n* Streamlined ATS optimization tools, resulting in a 30% increase in resume visibility\n* Built a robust backend in Python, reducing downtime by 20% and enhancing scalability\n* Managed cross-functional teams, improving project delivery time by 25%\n\n**Paintify**\nA & H Enterprise, June 2023 - August 2023\n* Developed an e-commerce platform with generative AI customer service, increasing user engagement by 40%\n* Integrated Shopify as the backend platform for scalability and secure transactions\n* Designed a visually appealing and user-friendly frontend using Next.js and Tailwind CSS\n* Reduced user onboarding time by 25% and retention rates by 20%, contributing to a 15% growth in monthly recurring revenue\n* Improved loading speed by 30% through code optimization and image compression techniques\n\n**Education**\n**Bachelor's in Computer Science**\nFAST NUCES KARACHI, Karachi, PK\nExpected Graduation: 2025\n\n**Skills**\n\n* Programming Languages: C++, C, Python, JavaScript\n* Frameworks and Libraries: FastAPI, ReactJS, Next.js, Framer Motion, Tailwind CSS\n* Databases: SQL, PostgreSQL\n* Development Tools: Docker, Git\n* E-commerce Platforms: Headless Shopify\n* Content Management Systems: Sanity\n* AI and Machine Learning: Generative AI, Natural Language Processing\n\n**Improvements:**\n\n* **Quantified impact:** Added specific metrics to demonstrate the impact of your work, e.g., \"Increased user acquisition by 45%\" instead of \"Boosted user acquisition through AI-driven features.\"\n* **Removed weak action verbs:** Replaced words like \"functioned,\" \"directed,\" and \"led\" with stronger verbs that highlight your accomplishments, e.g., \"developed,\" \"implemented,\" and \"managed.\"\n* **Avoided responsibility-oriented words:** Focused on describing what you achieved rather than what you were responsible for, e.g., \"Developed frontend solutions\" instead of \"Responsible for developing frontend solutions.\"\n* **Proofread for errors:** Corrected grammatical and spelling errors throughout the resume.\n* **Added a summary:** Included a brief summary section to provide an overview of your skills, experience, and career goals.\n* **Reformatted project descriptions:** Adjusted the formatting of the project descriptions to use bullet points and ensure consistency in punctuation and spacing.\n* **Unified dates:** Used a consistent date format throughout the resume (January 2023 - December 2023).\n* **Removed unnecessary details:** Omitted personal details such as your address and gender.\n* **Replaced embedded link:** Provided the full URL for your personal website instead of embedding a link."]
  },
])

    convo.send_message(f"""Remeber these are complusory keypoints in making a ats optimized resume .
                        If you find anything against it you have to correct it and rewrite all the
                        resume from start.Below is the resume . Analyze it and improve if nessasry.
                         {resume}""")
    response1 = (convo.last.text)

    # data send to openai for converting resume in json
    response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": """You are an expert in making text into json format.here is the foramt of json .
     {
  "resume": {
    "experience": {
      "title": "Front-End Developer | Brilliant IT Solutions | ",
      "date": "Apr 2022 – Jan 2024 | ",
      "resident": "Karachi, PK",
      "content": {
        "1": "Collaborated within a 10-member team to deliver a high-load project utilizing Next.js, React, and generative AI algorithms.",
        "2": "Implemented React framework for dynamic user interfaces, ensuring seamless data updates and a 30% performance improvement.",
        "3": "Leveraged Next.js for server-side rendering, effectively managing high traffic volumes. Spearheaded the integration of generative AI, automating manual tasks by 50% and boosting project performance metrics by 15%.",
        "4": "Crafted cross-device and cross-browser compatible front-end solutions, adhering to responsive design principles for optimal user experience."
      }
    },
    "projects": [
      {
        "name": "Portfolio",
        "link": "https://www.abdulhadi.info/",
        "description": "Developed a modern personal portfolio website using Next.js, Tailwind CSS, and Sanity CMS, showcasing web development expertise. Integrated an AI-powered chatbot using OpenAI to provide interactive visitor engagement. Achieved a 40% reduction in loading time and a 25% increase in user retention through Next.js front-end optimization."
      },
      {
        "name": "Intelliverse",
        "link": "https://sass-mu-six.vercel.app/",
        "description": "Led the development of an AI-driven SaaS platform for professionals and students, optimizing LinkedIn profiles and driving a 45% increase in user acquisition and 20% improvement in user satisfaction. Implemented AI-powered features, boosting user engagement by 40% and streamlining ATS optimization tools for a 30% increase in resume visibility. Enabled seamless LinkedIn content creation and sharing functionalities. Developed a robust Python backend, reducing downtime by 20% and ensuring scalability. Led cross-functional teams, accelerating project delivery by 25%."
      },
      {
        "name": "Paintify",
        "link": "https://nextjs-commerce-azure-chi.vercel.app/",
        "company": "A & H Enterprise",
        "date": "Jun 2023 – Aug 2023",
        "description": "Launched an e-commerce platform with generative AI customer service, resulting in a 40% increase in user engagement. Integrated Shopify for robust product management and secure transactions. Designed a user-friendly Next.js and Tailwind CSS front-end, reducing user onboarding time by 25% and increasing retention rates by 20%, contributing to a 15% growth in monthly recurring revenue. Optimized code and implemented image compression techniques, improving loading speed by 30% and significantly boosting search engine rankings."
      }
    ],
    "education": {
      "degree": "Bachelor of Computer Science",
      "university": "FAST NUCES Karachi",
      "date": "Expected 2025",
      "location": "Karachi, PK"
    },
    "skills": {
      "programming_languages": ["C++", "C", "Python", "Javascript"],
      "frameworks_libraries": ["FastAPI", "ReactJS", "Next.js", "Framer Motion", "Tailwind CSS"],
      "databases": ["SQL", "PostgreSQL"],
      "development_tools": ["Docker", "Git"],
      "e-commerce_platforms": ["Headless Shopify"],
      "cms": ["Sanity"],
      "ai_machine_learning": ["Generative AI"]
    }
  }
} """},
    {"role": "user", "content": f"""Convert this into json foramt given above{response1}"""},
  ]
)

    return response.choices[0].message.content

     

@app.post("/api/headline")
def get_headline(headline: Annotated[str, Depends(headline_check)], authorization : Annotated[bool , Depends(check_token)]):
    if authorization == True :
        return {'Data' : headline}
    else :
        return {'Failed' : 'Invalid Token'} 



@app.post("/api/profile")
def get_profile(profile : Annotated[str, Depends(check_profile)], authorization : Annotated[bool , Depends(check_token)]):
    if authorization == True :
        return {'Data' : profile}
    else :
        return {'Failed' : 'Invalid Token'} 




@app.post("/api/banner")
def check_banner1(banner : Annotated[str, Depends(check_banner)] , authorization : Annotated[bool , Depends(check_token)]):
    if authorization == True :
        return {'Data' : banner}
    else :
        return {'Failed' : 'Invalid Token'} 
    

@app.post("/api/resume")
def check_resume(resume: Annotated[str , Depends(check_resume)]):
    return {'Data' : resume}
    
    
# @app.post("/api/profile_data")
# def get_data(Data : Annotated[str, Depends(get_profile_data)] , authorization : Annotated[bool , Depends(check_token1)]):
#     if authorization == True :
#         return {'Data' : Data}
#     else :
#         return {'Failed' : 'Invalid Token . To Access this api contact Abdul hadi'} 
            
            
    

    
    
    




    
    
