-- This procedure aim to fully parse raw json to a column based table (the data is still raw)
-- from table landing.raw_products -> public.raw_parsed_products

CREATE OR REPLACE PROCEDURE raw_json_to_parsed_product()
AS $$
DECLARE
    json_data JSONB;
    parsed_data JSONB;
    record_id INTEGER;
    current_invoice_no VARCHAR(255);
    duplicate_key_count INTEGER := 0;
BEGIN
    -- Iterate over unprocessed records in the landing table
    FOR record_id IN (SELECT id FROM landing.raw_products WHERE processed = FALSE) LOOP
        -- Retrieve raw JSON data for the current record
        SELECT data INTO json_data
        FROM landing.raw_products
        WHERE id = record_id;

        -- Check if there is data to process
        IF json_data IS NOT NULL THEN
            -- Parse JSON data into a structured format
            BEGIN
                parsed_data := json_data;
                current_invoice_no := parsed_data->>'InvoiceNo';

                -- Insert parsed data into the public table
                BEGIN
                    INSERT INTO landing.raw_parsed_products (country, quantity, invoice_no, stock_code, unit_price, customer_id, description, invoice_date)
                    VALUES (
                        parsed_data->>'Country',
                        (parsed_data->>'Quantity')::INTEGER,
                        current_invoice_no,
                        parsed_data->>'StockCode',
                        (parsed_data->>'UnitPrice')::NUMERIC,
                        parsed_data->>'CustomerID',
                        parsed_data->>'Description',
                        TO_TIMESTAMP(parsed_data->>'InvoiceDate', 'MM/DD/YYYY HH24:MI')
                    );

                    -- set this product to processed to avoid redoing it next time
                    UPDATE landing.raw_products
                    SET processed = TRUE
                    WHERE id = record_id;

                EXCEPTION
                    WHEN unique_violation THEN
                        -- Counting the amount of duplicates
                        duplicate_key_count := duplicate_key_count + 1;
                END;

            EXCEPTION
                WHEN OTHERS THEN
                    -- Log errors and continue with the loop
                    RAISE NOTICE 'Error processing record % with InvoiceNo %: %', record_id, current_invoice_no, SQLERRM;
            END;

        ELSE
            RAISE NOTICE 'No new raw JSON data to process.';
        END IF;
    END LOOP;

    -- Print out the amount of duplicates
    RAISE NOTICE 'Duplicates in the import: %', duplicate_key_count;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in raw_json_to_parsed_product: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
