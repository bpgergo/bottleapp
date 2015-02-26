
create table days (
  nap integer not null,
  pair smallint not null,
  state varchar(8),
  url varchar(240),
constraint fdx primary key (nap)
);

create table nevek (
  id integer not null,
  name varchar(24) not null,
  lev smallint not null,
  point double precision,
  play integer,
  kmp double precision,
constraint nd0 primary key (id),
constraint nd1 unique (name)
) CHARSET=UTF8;

create table hist (
  id integer not null,
  nap integer not null,
  score varchar(4),
  meg double precision,
  lev smallint not null,
  point double precision,
  kmp double precision,
constraint td1 unique (id,nap)
  );


insert into nevek values (3, 'Nagy Jozsef', 3, 3.3, 4, 3.5);

insert into nevek values (2, 'Nagy Laci', 2, 2.3, 3, 2.5);

insert into nevek values (1, 'Kiss Jozsef', 1, 1.3, 2, 1.5);


create table page (
    id serial not null,
    url varchar(250) not null,
    ts timestamp not null,
    constraint pk_page primary key (id),
    constraint uniq_page unique (url)
) CHARSET=UTF8;

create table ranks (
  id serial not null,
  page_id BIGINT UNSIGNED not null,
  rank integer not null,
  pair integer not null,
  score double precision not null,
  percentage double precision not null,
  name1 varchar(250) not null,
  name2 varchar(250) not null,
constraint pk_pair_rank primary key (id),
constraint fk_pair_rank_page foreign key (page_id) references page(id)
) CHARSET=UTF8;
