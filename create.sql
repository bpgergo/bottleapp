
create table days (
  nap integer not null,
  pair smallint not null,
  state varchar(8),
  url varchar(240),
constraint fdx primary key (nap)
);

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


create table nevek (
  id serial not null,
  name varchar(250) not null,
  lev smallint ,
  point double ,
  play integer,
  kmp double,
constraint nd0 primary key (id),
constraint nd1 unique (name)
)
CHARSET=UTF8;


create table alias(
id serial not null,
alias varchar(250) not null,
name varchar(250) not null,
generator varchar(250) ,
approved integer default 0,
constraint pk_alias primary key (id),
constraint uk_alias unique (alias, name, generator)
)
CHARSET=UTF8;




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
  score double not null,
  percentage double not null,
  tie integer,
  name1 varchar(250) not null,
  name2 varchar(250) not null,
  name3 varchar(250),
constraint pk_pair_rank primary key (id),
constraint fk_pair_rank_page foreign key (page_id) references page(id)
) CHARSET=UTF8;

