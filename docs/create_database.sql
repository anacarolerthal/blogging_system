CREATE TABLE IF NOT EXISTS BaseUser (
    id SERIAL PRIMARY KEY,
    username VARCHAR (50) unique not null,
    passw VARCHAR(50),
    email VARCHAR(50) unique NOT NULL,
    is_moderator BOOLEAN
    )
    

CREATE TABLE IF NOT EXISTS Post (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES baseuser(id),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    text_content TEXT,
    image text,
    CHECK (text_content IS NOT NULL OR image IS NOT NULL)
   )
   
CREATE TABLE IF NOT exists Reply (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES baseuser(id),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    text_content TEXT,
    image text,
    parent_post_id INTEGER references post(id)
    CHECK (text_content IS NOT NULL OR image IS NOT NULL)
   )   

   CREATE TABLE IF NOT EXISTS PostTag (
            tag_post_id SERIAL PRIMARY KEY,
            tag_id INTEGER REFERENCES tag(tag_id),
            post_id INTEGER REFERENCES post(id),
            UNIQUE(tag_id, post_id)
        )
        
  CREATE TABLE IF NOT EXISTS Tag (
        tag_id SERIAL PRIMARY KEY,
        tag_name TEXT UNIQUE NOT NULL
    )

  CREATE TABLE IF NOT EXISTS UserFollows (
                follow_id SERIAL PRIMARY KEY,
                follower_id INTEGER REFERENCES baseuser(id),
                followee_id INTEGER REFERENCES baseuser(id),
                UNIQUE(follower_id, followee_id)
            )
            
CREATE TABLE IF NOT EXISTS PostLikes (
                like_id SERIAL PRIMARY KEY,
                post_id INTEGER REFERENCES post(id),
                user_id INTEGER REFERENCES baseuser(id),
                UNIQUE(post_id, user_id)
            )    
            
CREATE TABLE IF NOT EXISTS BannedUsers (
    ban_id SERIAL PRIMARY KEY,
    banner_id INTEGER REFERENCES baseuser(id),
    banned_id INTEGER REFERENCES baseuser(id)
)            
    