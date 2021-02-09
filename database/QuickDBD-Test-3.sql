-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/gYJ0aK
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- physical ERD

CREATE TABLE "Milk_Type" (
    "id" serial   NOT NULL,
    "Type" varchar   NOT NULL,
    CONSTRAINT "pk_Milk_Type" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Store" (
    "id" serial   NOT NULL,
    "Store_Number" int   NOT NULL,
    "Store_Name" varchar   NOT NULL,
    "Store_Zipcode" int   NOT NULL,
    CONSTRAINT "pk_Store" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Milk" (
    "id" serial   NOT NULL,
    "Store_ID" int   NOT NULL,
    "product_id" int   NOT NULL,
    "Brand" varchar   NOT NULL,
    "Type_ID" int   NOT NULL,
    "features" array   NOT NULL,
    "size" varchar   NOT NULL,
    "category" varchar   NOT NULL,
    "image" varchar   NOT NULL,
    CONSTRAINT "pk_Milk" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Price_History" (
    "product_id" int   NOT NULL,
    "date" datetime   NOT NULL,
    "saleprice" float   NOT NULL,
    "price" float   NOT NULL,
    CONSTRAINT "pk_Price_History" PRIMARY KEY (
        "product_id","date"
     )
);

ALTER TABLE "Milk" ADD CONSTRAINT "fk_Milk_Store_ID" FOREIGN KEY("Store_ID")
REFERENCES "Store" ("id");

ALTER TABLE "Milk" ADD CONSTRAINT "fk_Milk_Type_ID" FOREIGN KEY("Type_ID")
REFERENCES "Milk_Type" ("id");

ALTER TABLE "Price_History" ADD CONSTRAINT "fk_Price_History_product_id" FOREIGN KEY("product_id")
REFERENCES "Milk" ("id");

