import os
import json
import requests

# CONFIG
GROQ_API_KEY = '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'
GROQ_MODEL = 'llama3-70b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# System prompt for Website Builder Agent
WEBSITE_BUILDER_PROMPT = """
You are a professional Website Builder Agent.

Your tasks:
- Create a clean, fully responsive, one-page HTML5 website based on the user's color theme, niche, and meta information.
- Include meta tags for SEO (title, description, keywords) inside the <head>.
- Include inline CSS or <style> inside the HTML to make it self-contained.
- Structure the site professionally: header, about section, services/products section, contact section, and footer.
- Match the style and wording appropriately to the niche.
- Make sure the layout looks good on mobile and desktop devices (basic responsiveness using simple CSS).
- Avoid external CSS or JS files — everything should be inside one HTML file.
"""

def query_groq_llm(color_theme, niche, meta_title, meta_description, meta_keywords):
    print("Generating website...")

    user_prompt = f"""
Please build a one-page HTML website for the following:

- Color Theme: {color_theme}
- Niche: {niche}
- Meta Title: {meta_title}
- Meta Description: {meta_description}
- Meta Keywords: {meta_keywords}

Ensure the website is fully responsive, self-contained (inline CSS), includes the SEO meta information, and has a professional structure with header, about, services, contact, and footer sections.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": WEBSITE_BUILDER_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3  # more factual, professional
    }

    response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        print(f"Error querying Groq LLM: {response.status_code}, {response.text}")
        return None

def save_website_to_file(website_html, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(website_html)
    print(f"🌐 Website saved as: {filename}")

def main():
    print("🌟 Welcome to the Website Builder Agent!")

    color_theme = input("Enter your preferred color theme (e.g., blue and white, black and gold): ").strip()
    niche = input("Enter your website's niche (e.g., bakery, fitness coach, event planner): ").strip()

    print("\n--- Meta Data for SEO ---")
    meta_title = input("Enter the meta title for your webpage (appears on browser tab): ").strip()
    meta_description = input("Enter the meta description (short summary for search engines): ").strip()
    meta_keywords = input("Enter meta keywords (comma-separated, e.g., bakery, cakes, pastries): ").strip()

    website_html = query_groq_llm(color_theme, niche, meta_title, meta_description, meta_keywords)

    if website_html:
        safe_niche = niche.replace(' ', '_').lower()
        output_file = f"{safe_niche}_website.html"
        save_website_to_file(website_html, output_file)

        print("\n✅ Website creation complete!")
        print(f"📁 You can now open {output_file} in your browser or upload it to your hosting platform.")
    else:
        print("❌ Failed to generate website. Please try again.")

if __name__ == "__main__":
    main()



# import os
# import json
# import requests

# # CONFIG
# GROQ_API_KEY = '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'
# GROQ_MODEL = 'llama3-70b-8192'
# GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# # System prompt for Website Builder Agent
# WEBSITE_BUILDER_PROMPT = """
# You are a professional Website Builder Agent.

# Your tasks:
# - Create a clean, fully responsive, one-page HTML5 website based on the user's color theme and business niche.
# - Include inline CSS or <style> inside the HTML to make it self-contained.
# - Structure the site professionally: header, about section, services/products section, contact section, and footer.
# - Match the style and wording appropriately to the niche.
# - Make sure the layout looks good on mobile and desktop devices (basic responsiveness using simple CSS).
# - Avoid external CSS or JS files — everything should be inside one HTML file.
# """

# def query_groq_llm(color_theme, niche):
#     print("Generating website...")

#     user_prompt = f"""
# Please build a one-page HTML website for the following:

# - Color Theme: {color_theme}
# - Niche: {niche}

# Ensure the website is fully responsive, self-contained (inline CSS), and professionally structured with header, about, services, contact, and footer sections.
# """

#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": GROQ_MODEL,
#         "messages": [
#             {"role": "system", "content": WEBSITE_BUILDER_PROMPT},
#             {"role": "user", "content": user_prompt}
#         ],
#         "temperature": 0.3  # more factual, professional
#     }

#     response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))

#     if response.status_code == 200:
#         return response.json()['choices'][0]['message']['content'].strip()
#     else:
#         print(f"Error querying Groq LLM: {response.status_code}, {response.text}")
#         return None

# def save_website_to_file(website_html, filename):
#     with open(filename, 'w', encoding='utf-8') as f:
#         f.write(website_html)
#     print(f"🌐 Website saved as: {filename}")

# def main():
#     print("🌟 Welcome to the Website Builder Agent!")

#     color_theme = input("Enter your preferred color theme (e.g., blue and white, black and gold): ").strip()
#     niche = input("Enter your website's niche (e.g., bakery, fitness coach, event planner): ").strip()

#     website_html = query_groq_llm(color_theme, niche)

#     if website_html:
#         safe_niche = niche.replace(' ', '_').lower()
#         output_file = f"{safe_niche}_website.html"
#         save_website_to_file(website_html, output_file)

#         print("\n✅ Website creation complete!")
#         print(f"📁 You can now open {output_file} in your browser or upload it to your hosting platform.")
#     else:
#         print("❌ Failed to generate website. Please try again.")

# if __name__ == "__main__":
#     main()
