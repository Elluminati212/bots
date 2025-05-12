import os
import re
import json
import shutil
import google.generativeai as genai
from pathlib import Path, PurePosixPath

# === CONFIG ===
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "AIzaSyB4Ims6KB3iEm3o7CITeTYd1QYt4_5Lw-U"
GEMINI_MODEL_NAME = "gemini-2.0-flash"

# Configure the Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)

print("🌐 Custom Website Builder Agent")

# === GET USER INPUT ===
tech = "react"
print(f"Using technology: {tech}")
desc = input("Describe your webpage in detail: ").strip()

# === PROMPTS ===
system_prompt_dynamic_webpage = """
You are an expert full-stack React developer. Generate a complete React application using Vite with well-organized components.
Create a dynamic and user-friendly webpage based on the user's description. Include:
1. A main App.jsx file
2. Necessary components in src/components
3. Tailwind CSS for styling
4. Interactive elements and modern UI/UX design
5. Placeholder content relevant to the description

Return a JSON object in a markdown code block with a 'files' array. Each file should have a 'path' and 'content'.
"""

user_prompt_dynamic_webpage = f"""
Create a dynamic webpage with the following description:

{desc}

Focus on making it interactive, visually appealing, and user-friendly. Use modern React practices and Tailwind CSS.
"""

# === SEND TO LLM ===
print(f"🧠 Querying Gemini LLM ({GEMINI_MODEL_NAME}) for the React app...")

model = genai.GenerativeModel(GEMINI_MODEL_NAME)
response = model.generate_content(
    [system_prompt_dynamic_webpage, user_prompt_dynamic_webpage],
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,
    )
)

if response.prompt_feedback and response.prompt_feedback.block_reason:
    raise Exception(f"Gemini API blocked the prompt: {response.prompt_feedback.block_reason}")

raw_content = response.text

if not raw_content:
    raise Exception("Empty response from Gemini API.")

# === PARSE RESPONSE ===
def extract_json_from_codeblock(text):
    match = re.search(r"```(?:json)?\s*({.*?})\s*```", text, re.DOTALL)
    if not match:
        raise ValueError("JSON code block not found in LLM response.")
    return match.group(1)

def clean_path(raw_path):
    return str(PurePosixPath(raw_path).relative_to("."))

base_dir = Path(f"{tech}_site")

try:
    with open("llm_output.md", "w", encoding="utf-8") as f:
        f.write(raw_content)

    json_text = extract_json_from_codeblock(raw_content)
    file_data = json.loads(json_text)

    files_to_write = [
        {"path": clean_path(file["path"]), "content": file["content"].strip()}
        for file in file_data.get("files", [])
        if file.get("path") and file.get("content")
    ]

    if not files_to_write:
        raise ValueError("No valid files found in LLM response.")

except Exception as e:
    print(f"Error processing LLM output: {e}")
    print("LLM response saved to llm_output.md for inspection.")
    exit(1)

# === WRITE FILES ===
if base_dir.exists():
    shutil.rmtree(base_dir)
base_dir.mkdir(parents=True)

for file in files_to_write:
    try:
        target_path = base_dir / file["path"]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(file["content"])
    except Exception as e:
        print(f"Error writing file {file['path']}: {e}")

print(f"✅ {len(files_to_write)} files written to `{base_dir}`.")

# === INSTALL DEPENDENCIES ===
print("📦 Installing dependencies...")
os.system(f"cd {base_dir} && npm install")

# === START PROJECT ===
print("🚀 Starting React dev server...")
os.system(f"cd {base_dir} && npm run dev")

print("✅ Custom React app setup complete!")
print("The dev server is now running. Access your custom webpage through the provided local URL.")


# #1st working code

# import os
# import re
# import json
# import shutil
# import requests
# import google.generativeai as genai
# from pathlib import Path, PurePosixPath

# # === CONFIG ===
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "AIzaSyB4Ims6KB3iEm3o7CITeTYd1QYt4_5Lw-U"  # Replace with your actual Gemini API key
# GEMINI_MODEL_NAME = "gemini-2.0-flash"

# # Configure the Gemini API key
# genai.configure(api_key=GOOGLE_API_KEY)

# print("🌐 Welcome to the Website Builder Agent (Iterative Approach)!")

# # === GET USER INPUT ===
# tech = "react"  # Force React for this example
# print(f"Using technology: {tech}")
# desc = input(f"Describe your webpage in detail for the homepage (e.g., name, key features, call to action, specific sections, desired interactions): ").strip()

# # === PROMPTS ===
# # system_prompt_homepage_enhanced = (
# #     "You are a senior full-stack React developer with expertise in UI/UX. Generate the complete file structure for a React application "
# #     "using Vite and well-organized components within the `src/components` directory. "
# #     "Create a `Homepage.jsx` component with the following sections based on the user's description: "
# #     "a dynamic hero section with a compelling call-to-action button, an 'About Us' section highlighting the club's history and mission, "
# #     "a 'Membership' section with clear benefits and a signup option, a 'Facilities' section showcasing available amenities (e.g., gym, pool, courts), "
# #     "a 'Contact Us' section with a functional contact form and contact details, and a visually appealing footer with social media links and copyright information. "
# #     "Use Tailwind CSS for a modern and clean vintage brown color theme with appropriate typography and spacing for readability. "
# #     "Incorporate basic interactive elements where suitable (e.g., hover effects on buttons, smooth scrolling for navigation). "
# #     "Include placeholder content that is relevant and engaging, along with image placeholders indicating the type of image needed. "
# #     "Ensure the generated code is well-structured, readable, and follows React best practices. "
# #     "Return a JSON object wrapped in a markdown code block with the `files` structure, including all necessary React components, styling, and the main `App.jsx`."
# # )

# # user_prompt_homepage_enhanced = (
# #     f"Create a full-fledged and interactive homepage for our sports club based on this detailed description:\n\n"
# #     f"{desc}\n\n"
# #     "Ensure the design is user-friendly and visually appealing with a modern take on a vintage brown theme using Tailwind CSS. "
# #     "Incorporate clear calls to action, smooth navigation between sections, and a functional contact form (even if it's just a placeholder for backend integration later). "
# #     "Provide realistic and engaging placeholder content for all sections, including benefits of membership, details about facilities, and contact information. "
# #     "Include image placeholders with descriptive names (e.g., 'hero-image.jpg', 'gym-facility.jpg'). "
# #     "Return only a JSON with `files`, each with relative `path` and `content`. Include all necessary React components, the main `App.jsx`, and any other relevant files for a basic working webpage. "
# #     "Wrap the entire JSON object in a markdown code block. No extra explanation."
# # )

# system_prompt_dynamic_webpage = (
#     "You are an expert full-stack React developer with a strong focus on creating dynamic, ultra-user-friendly web applications with the latest UI/UX design trends. "
#     "Generate the complete file structure for a modern React application using Vite and well-organized, reusable components within the `src/components` directory. "
#     "Create a `Homepage.jsx` component that serves as the main entry point, incorporating dynamic elements and the latest UI patterns based on the user's description. "
#     "Focus on creating a seamless and engaging user experience with the following considerations: "
#     "-   **Dynamic Content:** Design the architecture to easily integrate dynamic data. Include examples of how data could be fetched or updated (even if the actual data fetching logic is placeholder). "
#     "-   **Latest UI Trends:** Incorporate modern UI/UX patterns such as micro-interactions, subtle animations, smooth transitions, parallax scrolling (where appropriate), interactive carousels, engaging visual elements, and a focus on intuitive navigation. "
#     "-   **Ultra User-Friendliness:** Prioritize ease of use, clear calls to action, intuitive workflows, and excellent responsiveness across all devices. Ensure accessibility (semantic HTML, ARIA attributes). "
#     "-   **Component-Based Architecture:** Create modular and reusable React components for different sections and interactive elements. "
#     "-   **State Management (Basic):** If the dynamic elements require basic state management for UI updates, include simple examples using `useState` or `useContext`. "
#     "-   **Styling:** Utilize Tailwind CSS for a contemporary and visually appealing design. Focus on a clean, modern aesthetic with attention to typography, spacing, and color palettes that enhance usability. "
#     "-   **Sections (Dynamic based on description):** Based on the user's input, create relevant sections. Think beyond static content and consider how these sections could display dynamic information. "
#     "-   **Interactive Elements:** Implement interactive elements that enhance user engagement, such as dynamic forms with validation, interactive maps, filterable lists, and real-time updates (placeholder examples). "
#     "-   **Performance:** Structure the code with performance in mind (e.g., lazy loading of components/images - as placeholders). "
#     "-   **Return a JSON object wrapped in a markdown code block with the `files` structure, including all necessary React components, styling, any utility functions, and the main `App.jsx` with routing setup if multiple views are implied by the description.**"
# )

# user_prompt_dynamic_webpage = (
#     f"Create a dynamic and ultra user-friendly webpage with the latest UI/UX design for the following:\n\n"
#     f"{desc}\n\n"
#     "Focus on making the webpage highly interactive, visually stunning, and incredibly easy to use. Incorporate the latest UI trends and design patterns to create a cutting-edge user experience. "
#     "Think about how content can be dynamically updated and how users can interact with the page in engaging ways. "
#     "Generate all necessary React components, the main `App.jsx` (with basic routing if needed), any utility functions, and all associated styling using Tailwind CSS. "
#     "Ensure the code is well-structured, efficient, and demonstrates best practices for building modern React applications with dynamic capabilities. "
#     "Include placeholder examples of dynamic data integration and interactive elements. "
#     "Wrap the entire JSON object in a markdown code block. No extra explanation."
# )


# # === SEND TO LLM ===
# print(f"🧠 Querying Gemini LLM ({GEMINI_MODEL_NAME}) for the enhanced React app and Homepage...")

# model = genai.GenerativeModel(GEMINI_MODEL_NAME)
# response_homepage = model.generate_content(
#     [system_prompt_dynamic_webpage, user_prompt_dynamic_webpage],
#     generation_config=genai.types.GenerationConfig(
#         temperature=0.6,  # Slightly higher for more creative and complete output
#     )
# )

# if response_homepage.prompt_feedback and response_homepage.prompt_feedback.block_reason:
#     print(f"❌ Gemini API blocked the prompt: {response_homepage.prompt_feedback.block_reason}")
#     print("Falling back to a simpler React app...")
#     base_dir = Path(f"{tech}_site")
#     if base_dir.exists():
#         shutil.rmtree(base_dir)
#     os.chdir(base_dir.parent)
#     os.system(f"npx create-{tech}-app {base_dir.name}")
#     exit(0)

# raw_content_homepage = response_homepage.text

# if not raw_content_homepage:
#     print("❌ Empty response from Gemini API (Homepage).")
#     print("Falling back to a simpler React app...")
#     base_dir = Path(f"{tech}_site")
#     if base_dir.exists():
#         shutil.rmtree(base_dir)
#     os.chdir(base_dir.parent)
#     os.system(f"npx create-{tech}-app {base_dir.name}")
#     exit(0)

# # === PARSE RESPONSE ===
# def extract_json_from_codeblock(text):
#     match = re.search(r"```(?:json)?\s*({.*?})\s*```", text, re.DOTALL)
#     if not match:
#         raise ValueError("JSON code block not found.")
#     return match.group(1)

# def clean_path(raw_path):
#     try:
#         return str(PurePosixPath(raw_path).relative_to("."))
#     except Exception:
#         return None

# def is_valid_file(file_entry):
#     return isinstance(file_entry, dict) and \
#            isinstance(file_entry.get("path"), str) and \
#            isinstance(file_entry.get("content"), str)

# base_dir = Path(f"{tech}_site")

# try:
#     with open("last_llm_output_homepage.md", "w", encoding="utf-8") as f:
#         f.write(raw_content_homepage)

#     json_text_homepage = extract_json_from_codeblock(raw_content_homepage)

#     # Load JSON or fallback to literal_eval
#     try:
#         file_data_homepage = json.loads(json_text_homepage)
#     except json.JSONDecodeError:
#         import ast
#         print("⚠️ Fixing malformed JSON (Homepage) using ast.literal_eval...")
#         file_data_homepage = ast.literal_eval(json_text_homepage)

#     # Clean file entries
#     seen_paths = set()
#     files_to_write = []
#     for file in file_data_homepage.get("files", []):
#         path = file.get("path", "").strip()
#         content = file.get("content", "")
#         if path and content and path not in seen_paths:
#             files_to_write.append({ "path": path, "content": content.strip() })
#             seen_paths.add(path)

# except Exception as e:
#     print(f"⚠️ Invalid or unreadable LLM output (Homepage). Error: {e}")
#     print("📄 LLM response (Homepage) saved to last_llm_output_homepage.md")
#     print(f"💡 Falling back to create-{tech}-app...")

#     if base_dir.exists():
#         shutil.rmtree(base_dir)
#     os.chdir(base_dir.parent)
#     os.system(f"npx create-{tech}-app {base_dir.name}")
#     exit(0)

# # === WRITE FILES ===
# if base_dir.exists():
#     shutil.rmtree(base_dir)
# base_dir.mkdir(parents=True)

# valid_files = 0
# for file in files_to_write:
#     safe_path = clean_path(file["path"])
#     if not safe_path:
#         continue
#     try:
#         target_path = base_dir / safe_path
#         target_path.parent.mkdir(parents=True, exist_ok=True)
#         with open(target_path, "w", encoding="utf-8") as f:
#             f.write(file["content"])
#         valid_files += 1
#     except Exception as e:
#         print(f"⚠️ Error writing file {safe_path}: {e}")
#         continue

# if valid_files == 0:
#     print("⚠️ All LLM files for the homepage were invalid. Reverting to base project...")
#     os.chdir(base_dir.parent)
#     os.system(f"npx create-{tech}-app {base_dir.name}")
#     exit(0)

# print(f"✅ {valid_files} custom files written to `{base_dir}`.")

# # === INSTALL DEPENDENCIES ===
# if tech == "react":
#     print("📦 Installing dependencies...")
#     os.system(f"cd {base_dir} && npm install")

# # === OPTIONAL: START PROJECT ===
# if tech == "react":
#     print("🚀 Starting React dev server...")
#     os.system(f"cd {base_dir} && npm run dev") # Assuming Vite setup

# print("✅ Enhanced React app with homepage setup complete!")
# print("Next steps: Run the dev server and further develop individual components/pages, adding more advanced interactivity and styling.")

#-------------------------------------------------------------------------------------------------------------------------------------------

# import os
# import re
# import json
# import shutil
# import google.generativeai as genai
# from pathlib import Path, PurePosixPath

# # === CONFIG ===
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "AIzaSyDTrsMXUu8Qsl7HRFEfpJwWQK5Ru2_pbeA"  # Replace with your actual Gemini API key
# GEMINI_MODEL_NAME = "gemini-2.0-flash"

# # Configure the Gemini API key
# genai.configure(api_key=GOOGLE_API_KEY)

# print("🌐 Versatile Website Builder Agent (Iterative Approach)!")

# # === GET USER INPUT ===
# tech = "react"  # Force React for this example
# print(f"Using technology: {tech}")
# desc = input("Describe the webpage you want to create in detail (e.g., type of website, purpose, target audience, key features, desired sections, specific design elements, and any interactive requirements): ").strip()

# # === PROMPTS ===
# system_prompt_webpage_builder = (
#     "You are a senior full-stack React developer with extensive experience in modern web design and UI/UX principles. Your task is to generate the complete file structure for a React application "
#     "using Vite and well-organized, reusable components within the `src/components` directory.  The goal is to create a dynamic and engaging webpage based on the user's description. "
#     "Consider modern design trends, accessibility, and user experience best practices.  The webpage should be responsive and adapt well to different screen sizes. "
#     "Based on the user's description, generate appropriate sections, content, and interactive elements. Use the following guidelines: "
#     "-   **Structure:** Create a clear and logical structure with reusable components.  Use semantic HTML and appropriate ARIA roles for accessibility. "
#     "-   **Styling:** Apply a modern and visually appealing design using Tailwind CSS.  Incorporate contemporary design elements such as subtle animations, smooth transitions, consistent spacing, and a well-defined color palette.  Prioritize readability and visual hierarchy. "
#     "-   **Interactivity:** Include interactive elements to enhance user engagement.  This could include interactive forms, dynamic content updates, client-side validation, and appropriate feedback mechanisms. "
#     "-   **Content:** Generate placeholder content that is relevant, engaging, and tailored to the website's purpose.  Use clear and concise language. "
#     "-   **Images/Media:** Incorporate image and media placeholders with descriptive names and appropriate alt text. "
#     "-   **Sections:** Based on the user's description, create relevant sections.  Common sections include: "
#     "    -   Hero Section: A prominent section at the top of the page with a clear call to action. "
#     "    -   About Us: Information about the organization, company, or individual. "
#     "    -   Services/Products: Details about offerings. "
#     "    -   Features: Key features of the product or service. "
#     "    -   Portfolio/Projects: Examples of past work. "
#     "    -   Testimonials: User feedback. "
#     "    -   Contact Us: A form and contact information. "
#     "    -   FAQ: Frequently asked questions. "
#     "    -   Blog/News: Updates and articles. "
#     "    -   Team: Information about the team members. "
#     "    -   Pricing: Plans and costs. "
#     "    -   Footer: Copyright, social links, and other general information. "
#     "-   **Components:** Design reusable React components for common elements such as buttons, forms, navigation, cards, and sections. "
#     "-  **App.jsx**: create a main App.jsx file that uses the components"
#     "Return a JSON object wrapped in a markdown code block with the `files` structure, including all necessary React components, styling, and the main `App.jsx`."
# )

# user_prompt_webpage_builder = (
#     f"Create a modern and user-friendly webpage based on the following description:\n\n"
#     f"{desc}\n\n"
#     "Focus on creating a visually appealing and highly interactive experience. Use the latest features of Tailwind CSS and React to achieve a contemporary look and feel. "
#     "Incorporate best practices for web development, including accessibility, performance, and maintainability. "
#     "Generate all necessary React components, the main `App.jsx`, and any other required files for a complete, functional webpage. "
#     "Ensure that the generated code is well-structured, readable, and easy to extend. "
#     "Wrap the entire JSON object in a markdown code block. No extra explanation."
# )

# # === SEND TO LLM ===
# print(f"🧠 Querying Gemini LLM ({GEMINI_MODEL_NAME}) for the webpage...")

# model = genai.GenerativeModel(GEMINI_MODEL_NAME)
# response_homepage = model.generate_content(
#     [system_prompt_webpage_builder, user_prompt_webpage_builder],
#     generation_config=genai.types.GenerationConfig(
#         temperature=0.7,  # Slightly higher for more creative and complete output
#     )
# )

# if response_homepage.prompt_feedback and response_homepage.prompt_feedback.block_reason:
#     print(f"❌ Gemini API blocked the prompt: {response_homepage.prompt_feedback.block_reason}")
#     print("Falling back to a simpler React app...")
#     base_dir = Path(f"{tech}_site")
#     if base_dir.exists():
#         shutil.rmtree(base_dir)
#     os.chdir(base_dir.parent)
#     os.system(f"npx create-{tech}-app {base_dir.name}")
#     exit(0)

# raw_content_homepage = response_homepage.text

# if not raw_content_homepage:
#     print("❌ Empty response from Gemini API (Homepage).")
#     print("Falling back to a simpler React app...")
#     base_dir = Path(f"{tech}_site")
#     if base_dir.exists():
#         shutil.rmtree(base_dir)
#     os.chdir(base_dir.parent)
#     os.system(f"npx create-{tech}-app {base_dir.name}")
#     exit(0)

# # === PARSE RESPONSE ===
# def extract_json_from_codeblock(text):
#     match = re.search(r"```(?:json)?\s*({.*?})\s*```", text, re.DOTALL)
#     if not match:
#         raise ValueError("JSON code block not found.")
#     return match.group(1)

# def clean_path(raw_path):
#     try:
#         return str(PurePosixPath(raw_path).relative_to("."))
#     except Exception:
#         return None

# def is_valid_file(file_entry):
#     return isinstance(file_entry, dict) and \
#            isinstance(file_entry.get("path"), str) and \
#            isinstance(file_entry.get("content"), str)

# base_dir = Path(f"{tech}_site")

# try:
#     with open("last_llm_output_homepage.md", "w", encoding="utf-8") as f:
#         f.write(raw_content_homepage)

#     json_text_homepage = extract_json_from_codeblock(raw_content_homepage)

#     # Load JSON or fallback to literal_eval
#     try:
#         file_data_homepage = json.loads(json_text_homepage)
#     except json.JSONDecodeError:
#         import ast
#         print("⚠️ Fixing malformed JSON (Homepage) using ast.literal_eval...")
#         file_data_homepage = ast.literal_eval(json_text_homepage)

#     # Clean file entries
#     seen_paths = set()
#     files_to_write = []
#     for file in file_data_homepage.get("files", []):
#         path = file.get("path", "").strip()
#         content = file.get("content", "")
#         if path and content and path not in seen_paths:
#             files_to_write.append({ "path": path, "content": content.strip() })
#             seen_paths.add(path)

# except Exception as e:
#     print(f"⚠️ Invalid or unreadable LLM output (Homepage). Error: {e}")
#     print("📄 LLM response (Homepage) saved to last_llm_output_homepage.md")
#     print(f"💡 Falling back to create-{tech}-app...")

#     if base_dir.exists():
#         shutil.rmtree(base_dir)
#     os.chdir(base_dir.parent)
#     os.system(f"npx create-{tech}-app {base_dir.name}")
#     exit(0)

# # === WRITE FILES ===
# if base_dir.exists():
#     shutil.rmtree(base_dir)
# base_dir.mkdir(parents=True)

# valid_files = 0
# for file in files_to_write:
#     safe_path = clean_path(file["path"])
#     if not safe_path:
#         continue
#     try:
#         target_path = base_dir / safe_path
#         target_path.parent.mkdir(parents=True, exist_ok=True)
#         with open(target_path, "w", encoding="utf-8") as f:
#             f.write(file["content"])
#         valid_files += 1
#     except Exception as e:
#         print(f"⚠️ Error writing file {safe_path}: {e}")
#         continue

# if valid_files == 0:
#     print("⚠️ All LLM files for the webpage were invalid. Reverting to base project...")
#     os.chdir(base_dir.parent)
#     os.system(f"npx create-{tech}-app {base_dir.name}")
#     exit(0)

# print(f"✅ {valid_files} custom files written to `{base_dir}`.")

# # === INSTALL DEPENDENCIES ===
# if tech == "react":
#     print("📦 Installing dependencies...")
#     os.system(f"cd {base_dir} && npm install")

# # === OPTIONAL: START PROJECT ===
# if tech == "react":
#     print("🚀 Starting React dev server...")
#     os.system(f"cd {base_dir} && npm run dev") # Assuming Vite setup

# print("✅ Enhanced React app with homepage setup complete!")
# print("Next steps: Run the dev server and further develop individual components/pages, adding more advanced interactivity and styling.")