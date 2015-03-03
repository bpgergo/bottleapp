
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
name varchar(150) not null,
alias1 varchar(150) not null,
alias2 varchar(150) ,
alias3 varchar(150) ,
alias4 varchar(150) ,
alias5 varchar(150) ,
generator varchar(150) ,
approved integer default 0,
constraint pk_alias primary key (id),
constraint uniq_alias unique (name, alias1, alias2, alias3, alias4, alias5)
)
CHARSET=UTF8;

create table crawl (
    id serial not null,
    url varchar(250) not null,
    ts timestamp not null,
    constraint pk_page primary key (id),
    constraint uniq_crawl unique (url)
) CHARSET=UTF8;


create table page (
    id serial not null,
    crawl_id BIGINT unsigned not null,
    url varchar(250) not null,
    ts timestamp not null,
    constraint pk_page primary key (id),
    constraint uniq_page unique (url),
    constraint fk_page_crawl foreign key (crawl_id) references crawl(id)
) CHARSET=UTF8;

create table ranks (
  id serial not null,
  page_id BIGINT unsigned not null,
  rank integer not null,
  pair integer not null,
  score double not null,
  percentage double not null,
  tie integer,
  original_name1 varchar(250) not null,
  original_name2 varchar(250) not null,
  original_name3 varchar(250),
  name1_id bigint unsigned,
  name2_id bigint unsigned,
  name3_id bigint unsigned,
constraint pk_ranks primary key (id),
constraint fk_ranks_page foreign key (page_id) references page(id),
constraint fk_ranks_name1 foreign key (name1_id) references nevek(id),
constraint fk_ranks_name2 foreign key (name2_id) references nevek(id),
constraint fk_ranks_name3 foreign key (name3_id) references nevek(id)
) CHARSET=UTF8;
