CREATE DATABASE movierec_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT,
    imdb_rating DECIMAL(3,1),
    director VARCHAR(255),
    synopsis TEXT,
    FULLTEXT (title)
);
CREATE TABLE genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL ,
    unique(name)
);
create table movie_genres(
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
);

create table actors(
    id int auto_increment primary key,
    name varchar(100) not nul 
);
create table movie_actors(
    movie_id int ,
    actor_id int ,
    PRIMARY KEY(movie_id,actor_id),
    foreign key(movie_id) references movies(id) on delete cascade,
    foreign key(actor_id) references actors(id) on delete cascade
);
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE watched (
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rating TINYINT,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);
create table search_history(
    id int auto_increment primary key,
    user_id int not null,
    query varchar(255) not null,
    created_at timestamp default current_timestamp,
    foreign key(user_id) references users(id) on delete cascade
);

