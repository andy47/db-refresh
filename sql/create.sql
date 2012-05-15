CREATE TABLE source_files (
    id                            INTEGER       NOT NULL AUTO_INCREMENT
   ,file_name                     VARCHAR(200)
   ,load_date                     DATE
   ,start_date                    DATE
   ,finish_date                   DATE
   ,record_count                  INTEGER
   ,PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE policy_transactions (
    id                            INTEGER       NOT NULL AUTO_INCREMENT
   ,file_id                       INTEGER       REFERENCES source_files (id)
   ,record_number                 INTEGER       NOT NULL
   ,policy_number                 varchar(20)   NOT NULL
   ,insured_name                  varchar(4000) NOT NULL
   ,transaction_type              varchar(2)    NOT NULL
   ,transaction_date              date          NOT NULL
   ,from_date                     date          NOT NULL
   ,to_date                       date          NOT NULL
   ,broker_group                  varchar(255)  DEFAULT NULL
   ,staff                         INTEGER
   ,industry_code                 INTEGER       NOT NULL
   ,annual_revenue                INTEGER       NOT NULL
   ,section_number                varchar(2)    NOT NULL
   ,section_type                  varchar(2)    NOT NULL
   ,layer_limit                   decimal(13,2) NOT NULL
   ,excess                        decimal(13,2) NOT NULL
   ,gross_premium                 decimal(13,2) NOT NULL
   ,premium_gst                   decimal(13,2) NOT NULL
   ,stamp_duty                    decimal(13,2) DEFAULT NULL
   ,commission                    decimal(13,2) NOT NULL
   ,commission_gst                decimal(13,2) NOT NULL
   ,invoice_number                varchar(50)   NOT NULL
   ,PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
