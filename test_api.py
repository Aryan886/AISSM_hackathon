from google import genai

client = genai.Client(api_key="AIzaSyDbXHjMgmp_BcwK74LPVjCpkwSlHt72fWs")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello"
)

print(response.text)
