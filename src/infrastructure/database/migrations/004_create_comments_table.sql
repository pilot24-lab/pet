create table if not exists comments (
    id serial primary key,
    user_id integer not null,
    comments text not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp

    constraint fk_comments_user
        foreign key (user_id)
        references users(id)
        on delete cascade
);

create index of not exists idx_users_id on comments(user_id)