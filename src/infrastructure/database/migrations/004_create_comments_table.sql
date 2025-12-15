create table if not exists comments (
    id serial primary key,
    user_id integer references users(id) not null,
    comment text not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp   
);

create index if not exists idx_users_id on comments(user_id);