#
# File: Populate.sql
# Author: Andrew J Todd esq (andy47@halfcooked.com)
# Date: 2011.10.25
# Purpose: Populate tables used to test my db_refresh utility

INSERT INTO source_files 
  (file_name, load_date, start_date, finish_date, record_count)
VALUES
  ('policy_test_1', '2011-03-01', '2011-03-01', '2011-03-31', 4),
  ('policy_test_2', '2011-04-01', '2011-04-01', '2011-04-30', 3),
  ('policy_test_3', '2011-05-01', '2011-05-01', '2011-05-31', 2)
;

INSERT INTO policy_transactions
  (file_id, record_number, policy_number, insured_name, transaction_type, transaction_date, from_date, to_date, staff, industry_code, annual_revenue, section_number, section_type, layer_limit, excess, gross_premium, premium_gst, stamp_duty, commission, commission_gst, invoice_number )
VALUES
	(1, 1, 'BPP03-0743', 'ICC Holdings Pty Limited; Illawarra Coke Company Pty Ltd', 'RE', '2010-11-22', '2010-11-01', '2011-11-01', 73, 1709, 0, 'S1', 'SL', 2000000.00, 20000.00, 14400.00, 1296.00, 1283.04, 2088.00, 208.80, '000029176'),
	(1, 2, 'BPP03-0743', 'ICC Holdings Pty Limited; Illawarra Coke Company Pty Ltd', 'RE', '2010-11-22', '2010-11-01', '2011-11-01', 73, 1709, 0, 'S2', 'DC', 2000000.00, 20000.00, 7600.00, 684.00, 677.16, 1102.00, 110.20, '000029176'),
	(1, 3, 'BPP03-0743', 'ICC Holdings Pty Limited; Illawarra Coke Company Pty Ltd', 'RE', '2010-11-22', '2010-11-01', '2011-11-01', 73, 1709, 0, 'S3', 'EP', 2000000.00, 2500.00, 2222.22, 200.00, 198.00, 322.22, 32.22, '000029176'),
	(2, 1, 'BPP03-0743', 'ICC Holdings Pty Limited; Illawarra Coke Company Pty Ltd', 'CN', '2011-01-20', '2010-11-01', '2011-11-01', 73, 1709, 0, 'S1', 'SL', 2000000.00, 20000.00, -14400.00, -1296.00, -1283.04, -2088.00, -208.80, '000029436'),
	(2, 2, 'BPP03-0743', 'ICC Holdings Pty Limited; Illawarra Coke Company Pty Ltd', 'CN', '2011-01-20', '2010-11-01', '2011-11-01', 73, 1709, 0, 'S2', 'DC', 2000000.00, 20000.00, -7600.00, -684.00, -677.16, -1102.00, -110.20, '000029436'),
	(2, 3, 'BPP03-0743', 'ICC Holdings Pty Limited; Illawarra Coke Company Pty Ltd', 'CN', '2011-01-20', '2010-11-01', '2011-11-01', 73, 1709, 0, 'S3', 'EP', 2000000.00, 2500.00, -2222.22, -200.00, -198.00, -322.22, -32.22, '000029436'),
	(3, 1, 'BPP03-0743', 'ICC Holdings Pty Limited; Illawarra Coke Company Pty Ltd', 'RI', '2011-01-20', '2010-11-01', '2011-11-01', 73, 1709, 0, 'S1', 'SL', 2000000.00, 20000.00, 12960.00, 1296.00, 1283.04, 3175.20, 317.52, '000029438'),
	(3, 2, 'BPP03-0743', 'ICC Holdings Pty Limited; Illawarra Coke Company Pty Ltd', 'RI', '2011-01-20', '2010-11-01', '2011-11-01', 73, 1709, 0, 'S2', 'DC', 2000000.00, 20000.00, 6840.00, 684.00, 677.16, 1675.80, 167.58, '000029438'),
	(3, 3, 'BPP03-0743', 'ICC Holdings Pty Limited; Illawarra Coke Company Pty Ltd', 'RI', '2011-01-20', '2010-11-01', '2011-11-01', 73, 1709, 0, 'S3', 'EP', 2000000.00, 2500.00, 2000.00, 200.00, 198.00, 490.00, 49.00, '000029438'),
	(2, 4, 'BPP08-0051', 'Dennis Savage & Jodie Savage T/As D&J Savage Interstate Transport', 'RE', '2011-03-28', '2011-03-19', '2012-03-19', 0, 4610, 0, 'S1', 'SL', 1000000.00, 2000.00, 458.41, 45.84, 0.00, 112.31, 11.23, '000029741'),
	(2, 5, 'BPP08-0051', 'Dennis Savage & Jodie Savage T/As D&J Savage Interstate Transport', 'RE', '2011-03-28', '2011-03-19', '2012-03-19', 0, 4610, 0, 'S2', 'DC', 1000000.00, 2000.00, 400.00, 40.00, 0.00, 98.00, 9.80, '000029741'),
	(2, 6, 'BPP08-0051', 'Dennis Savage & Jodie Savage T/As D&J Savage Interstate Transport', 'RE', '2011-03-28', '2011-03-19', '2012-03-19', 0, 4610, 0, 'S3', 'EP', 1000000.00, 2000.00, 400.00, 40.00, 0.00, 98.00, 9.80, '000029741'),
	(3, 4, 'BPP08-0051', 'Dennis Savage & Jodie Savage T/As D&J Savage Interstate Transport', 'CN', '2011-05-20', '2011-03-19', '2012-03-19', 0, 4610, 0, 'S1', 'SL', 1000000.00, 2000.00, -458.41, -45.84, 0.00, -112.31, -11.23, '000030002'),
	(3, 5, 'BPP08-0051', 'Dennis Savage & Jodie Savage T/As D&J Savage Interstate Transport', 'CN', '2011-05-20', '2011-03-19', '2012-03-19', 0, 4610, 0, 'S2', 'DC', 1000000.00, 2000.00, -400.00, -40.00, 0.00, -98.00, -9.80, '000030002'),
	(3, 6, 'BPP08-0051', 'Dennis Savage & Jodie Savage T/As D&J Savage Interstate Transport', 'CN', '2011-05-20', '2011-03-19', '2012-03-19', 0, 4610, 0, 'S3', 'EP', 1000000.00, 2000.00, -400.00, -40.00, 0.00, -98.00, -9.80, '000030002'),
	(3, 7, 'BPP08-0051', 'Dennis Savage & Jodie Savage T/As D&J Savage Interstate Transport', 'RI', '2011-05-20', '2011-03-19', '2012-03-19', 0, 4610, 0, 'S1', 'SL', 1000000.00, 2000.00, 458.41, 45.84, 0.00, 112.31, 11.23, '000030003'),
	(3, 8, 'BPP08-0051', 'Dennis Savage & Jodie Savage T/As D&J Savage Interstate Transport', 'RI', '2011-05-20', '2011-03-19', '2012-03-19', 0, 4610, 0, 'S2', 'DC', 1000000.00, 2000.00, 400.00, 40.00, 0.00, 98.00, 9.80, '000030003'),
	(3, 9, 'BPP08-0051', 'Dennis Savage & Jodie Savage T/As D&J Savage Interstate Transport', 'RI', '2011-05-20', '2011-03-19', '2012-03-19', 0, 4610, 0, 'S3', 'EP', 1000000.00, 2000.00, 400.00, 40.00, 0.00, 98.00, 9.80, '000030003'),
	(1, 4, 'BPP10-0127', 'Hall & Prior Aged Care Group; Varna Pty Ltd ATF The Hall & Prior Nursing Home Group Unit Trust T/As Mosman Park Nursing Home, St Lukes Nursing Home, Tuohy Nursing Home; Fresh Fields Aged Care Pty Ltd T/As McDougall Park Nursing Home, Kensington Park Nursing Home, Rockingham Nursing Home; Varna Pty Ltd ATF the Mon Repos Unit Trust T/As Freshwater By Nursing Home; Hamersley Nursing Home (WA) Pty Ltd T/As Hamersley Nursing Home, Windsor Park Nursing Home; Danvero Pty Ltd ATF The Brookton Valley Aged Care Unit Trust T/As Clarence Estate Residential Aged Care, Concord Nursing Home, Belmont Nursing Home, Leighton Nursing Home; Fresh Fields Aged Care (NSW) No 1 Pty LTd T/As Alloa Aged Care, Vaucluse Aged Care Facility Caroline Chisholm Aged Care Facility, Glenwood Aged Care Facility, Meanaville Aged Care Facility, Sirius Cove Aged Care Facility; Fresh Fields Aged Care (NSW) No 2 Pty Ltd; Fresh Fields Aged Care (SA) No 1 Pty Ltd; Archmont Investments Pty Ltd; Jurien Unit Trust; Jurien Investments Pty Ltd; KEP Construction & Project Management Pty Ltd', 'RE', '2011-07-13', '2011-06-30', '2012-06-30', 400, 8601, 0, 'S1', 'SL', 5000000.00, 5000.00, 5775.00, 577.50, 278.54, 1414.88, 141.49, '000030415'),
	(1, 5, 'BPP10-0127', 'Hall & Prior Aged Care Group; Varna Pty Ltd ATF The Hall & Prior Nursing Home Group Unit Trust T/As Mosman Park Nursing Home, St Lukes Nursing Home, Tuohy Nursing Home; Fresh Fields Aged Care Pty Ltd T/As McDougall Park Nursing Home, Kensington Park Nursing Home, Rockingham Nursing Home; Varna Pty Ltd ATF the Mon Repos Unit Trust T/As Freshwater By Nursing Home; Hamersley Nursing Home (WA) Pty Ltd T/As Hamersley Nursing Home, Windsor Park Nursing Home; Danvero Pty Ltd ATF The Brookton Valley Aged Care Unit Trust T/As Clarence Estate Residential Aged Care, Concord Nursing Home, Belmont Nursing Home, Leighton Nursing Home; Fresh Fields Aged Care (NSW) No 1 Pty LTd T/As Alloa Aged Care, Vaucluse Aged Care Facility Caroline Chisholm Aged Care Facility, Glenwood Aged Care Facility, Meanaville Aged Care Facility, Sirius Cove Aged Care Facility; Fresh Fields Aged Care (NSW) No 2 Pty Ltd; Fresh Fields Aged Care (SA) No 1 Pty Ltd; Archmont Investments Pty Ltd; Jurien Unit Trust; Jurien Investments Pty Ltd; KEP Construction & Project Management Pty Ltd', 'RE', '2011-07-13', '2011-06-30', '2012-06-30', 400, 8601, 0, 'S2', 'DC', 5000000.00, 5000.00, 5355.00, 535.50, 258.28, 1311.98, 131.20, '000030415'),
	(1, 6, 'BPP10-0127', 'Hall & Prior Aged Care Group; Varna Pty Ltd ATF The Hall & Prior Nursing Home Group Unit Trust T/As Mosman Park Nursing Home, St Lukes Nursing Home, Tuohy Nursing Home; Fresh Fields Aged Care Pty Ltd T/As McDougall Park Nursing Home, Kensington Park Nursing Home, Rockingham Nursing Home; Varna Pty Ltd ATF the Mon Repos Unit Trust T/As Freshwater By Nursing Home; Hamersley Nursing Home (WA) Pty Ltd T/As Hamersley Nursing Home, Windsor Park Nursing Home; Danvero Pty Ltd ATF The Brookton Valley Aged Care Unit Trust T/As Clarence Estate Residential Aged Care, Concord Nursing Home, Belmont Nursing Home, Leighton Nursing Home; Fresh Fields Aged Care (NSW) No 1 Pty LTd T/As Alloa Aged Care, Vaucluse Aged Care Facility Caroline Chisholm Aged Care Facility, Glenwood Aged Care Facility, Meanaville Aged Care Facility, Sirius Cove Aged Care Facility; Fresh Fields Aged Care (NSW) No 2 Pty Ltd; Fresh Fields Aged Care (SA) No 1 Pty Ltd; Archmont Investments Pty Ltd; Jurien Unit Trust; Jurien Investments Pty Ltd; KEP Construction & Project Management Pty Ltd', 'RE', '2011-07-13', '2011-06-30', '2012-06-30', 400, 8601, 0, 'S3', 'EP', 5000000.00, 5000.00, 7770.00, 777.00, 374.76, 1903.65, 190.37, '000030415')
;

