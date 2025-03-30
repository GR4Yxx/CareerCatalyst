// Switch to admin database to create users
db = db.getSiblingDB("admin");

// Create admin user if it doesn't exist
if (!db.getUser("admin")) {
  db.createUser({
    user: "admin",
    pwd: process.env.MONGO_ROOT_PASSWORD || "password",
    roles: [{ role: "root", db: "admin" }],
  });
}

// Create CareerCatalyst database
db = db.getSiblingDB("career_catalyst");

// Create application user
if (!db.getUser("app_user")) {
  db.createUser({
    user: "app_user",
    pwd: process.env.MONGO_APP_PASSWORD || "app_password",
    roles: [{ role: "readWrite", db: "career_catalyst" }],
  });
}

// Create collections
db.createCollection("users");
db.createCollection("profiles");
db.createCollection("skills");
db.createCollection("user_skills");
db.createCollection("resumes");
db.createCollection("resume_versions");
db.createCollection("jobs");
db.createCollection("user_job_interactions");
db.createCollection("career_paths");
db.createCollection("user_career_plans");
db.createCollection("skill_relationships");

// Create fs.files and fs.chunks collections for GridFS
db.createCollection("fs.files");
db.createCollection("fs.chunks");

// Create indexes for performance
db.users.createIndex({ email: 1 }, { unique: true });
db.profiles.createIndex({ user_id: 1 }, { unique: true });
db.skills.createIndex({ name: 1 }, { unique: true });
db.user_skills.createIndex({ profile_id: 1, skill_id: 1 });
db.resumes.createIndex({ profile_id: 1 });
db.resumes.createIndex({ profile_id: 1, is_current: 1 });
db.resume_versions.createIndex({ resume_id: 1 });
db.resume_versions.createIndex({ job_id: 1 });
db.jobs.createIndex({ posted_date: -1 });
db.jobs.createIndex({ source: 1, source_id: 1 }, { unique: true });
db.user_job_interactions.createIndex(
  { user_id: 1, job_id: 1 },
  { unique: true }
);
db.user_career_plans.createIndex({ user_id: 1 });
db.skill_relationships.createIndex({ source_skill_id: 1, target_skill_id: 1 });

// Create TTL index for job cache expiration
db.jobs.createIndex({ cached_until: 1 }, { expireAfterSeconds: 0 });

// Create index on GridFS chunks
db.fs.chunks.createIndex({ files_id: 1, n: 1 }, { unique: true });
