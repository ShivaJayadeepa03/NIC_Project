import pandas as pd
import random

df = pd.read_csv("/static/latest_nic_dataset.csv")
df.columns = df.columns.str.strip()
df = df[['Sub-Class', 'Description']]
df.columns = ['NIC_code', 'Description']
df = df.dropna()

synthetic_data = []

templates = [
    "A company involved in {}",
    "Business specializing in {}",
    "Enterprise focused on {}",
    "Startup creating {}",
    "Company offering {}",
    "Organization engaged in {}",
    "Firm dealing with {}",
    "We provide {} services",
    "Our company works in {}",
    "Experts in {}",
    "Professionals handling {}",
    "Business dedicated to {}",
    "Company operating in {} sector",
    "Company working on {}",
    "Team focused on {}",
]

# Optional: add synonyms dictionary for tricky cases
synonyms_dict = {
    "Growing of wheat": ["wheat farming", "wheat cultivation", "wheat production"],
    "Development of mobile applications": ["mobile app development", "mobile software apps", "app creation"],
    # add more manually for other NIC descriptions
}

for idx, row in df.iterrows():
    nic = int(row['NIC_code'])
    desc = row['Description']
    
    # Get synonyms if available
    variations = synonyms_dict.get(desc, [desc])
    
    for variation in variations:
        # randomly pick templates to generate multiple sentences
        for _ in range(3):  # repeat 3 times for more variety
            template = random.choice(templates)
            sentence = template.format(variation)
            synthetic_data.append([nic, sentence])
            
    # Optional: if less than 30 sentences, repeat some random combinations
    while len([s for s in synthetic_data if s[0]==nic]) < 30:
        template = random.choice(templates)
        variation = random.choice(variations)
        synthetic_data.append([nic, template.format(variation)])

# Save to CSV
synthetic_df = pd.DataFrame(synthetic_data, columns=['NIC_code', 'Business_Description'])
synthetic_df.to_csv("nic_training_dataset.csv", index=False)

print("✅ Synthetic dataset with 30–50 examples per NIC code created!")