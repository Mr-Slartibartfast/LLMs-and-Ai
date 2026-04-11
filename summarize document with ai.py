def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize this clearly."},
            {"role": "user", "content": text}
        ]
    )

    return response.choices[0].message.content