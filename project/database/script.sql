create table if not exists users
(
  user_id       varchar(36) not null,
  first_name    varchar(30) not null,
  last_name     varchar(30) not null,
  user_password varchar(50) not null,
  email         varchar(30) not null,
  phone_number  char(30)    not null,
  address       varchar(50) not null,
  constraint users_user_id_uindex
    unique (user_id)
);

alter table users
  add primary key (user_id);

create table if not exists sessions
(
  session_id  varchar(36) not null,
  user_id     varchar(36) not null,
  expiry_date datetime    not null,
  constraint sessions_session_id_uindex
    unique (session_id),
  constraint sessions_users_user_id_fk
    foreign key (user_id) references users (user_id)
      on update cascade on delete cascade
);

alter table sessions
  add primary key (session_id);


