import os
import requests
from bs4 import BeautifulSoup
import openai


openai.api_key = "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"

def scrape_amazon_best_sellers():
    print("Scraping top products from Amazon...")
    url = "https://www.amazon.in/gp/bestsellers/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.select("._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y")[:3]

        if not titles:
            # fallback CSS selector
            titles = soup.select(".p13n-sc-truncate")[:3]

        return [t.get_text(strip=True) for t in titles]

    except Exception as e:
        print("Scraping failed:", e)
        return ["Smartphone", "Wireless Earbuds", "Fitness Band"]  # fallback mock data


def get_seo_keywords(product_name):
    base = product_name.split()[0]
    return [base, "buy online", "best price", "review"]


def generate_blog(product_name, keywords):
    prompt = f"""
    Write a 150-200 word SEO blog post about the product: "{product_name}".
    Include these SEO keywords naturally: {', '.join(keywords)}.
    Make it informative, engaging, and SEO-optimized.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("OpenAI API error:", e)
        return "Could not generate blog."


def save_blog_to_file(title, content):
    os.makedirs("blog_posts", exist_ok=True)
    filename = f"blog_posts/{title.replace(' ', '_')[:40]}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n\n")
        f.write(content)
    print(f"✅ Blog saved as: {filename}")


def main():
    products = scrape_amazon_best_sellers()
    for product in products:
        print(f"\n🔍 Product: {product}")
        keywords = get_seo_keywords(product)
        print(f"📈 Keywords: {keywords}")
        blog_content = generate_blog(product, keywords)
        print(f"✍️ Blog content generated.\n")
        save_blog_to_file(product, blog_content)

if __name__ == "__main__":
    main()
