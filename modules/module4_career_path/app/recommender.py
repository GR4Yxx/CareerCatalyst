# recommender.py

from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from sklearn.metrics.pairwise import cosine_similarity
from modules.module4_career_path.data_store import career_tracks, skill_pool

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings

def recommend_career_and_skills(job_tag: str, resume: str, top_k=3):
    user_input = job_tag + " " + resume
    user_embedding = embed_text(user_input)

    track_embeddings = torch.cat([embed_text(track) for track in career_tracks])
    track_sims = F.cosine_similarity(user_embedding, track_embeddings).numpy()
    top_tracks = [career_tracks[i] for i in track_sims.argsort()[-top_k:][::-1]]

    skill_embeddings = torch.cat([embed_text(skill) for skill in skill_pool])
    skill_sims = F.cosine_similarity(user_embedding, skill_embeddings).numpy()
    top_skills = [skill_pool[i] for i in skill_sims.argsort()[-top_k:][::-1]]

    return top_tracks, top_skills
