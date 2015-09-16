CREATE OR REPLACE FUNCTION sync_guide()
  RETURNS trigger AS
$BODY$
DECLARE
BEGIN
    PERFORM pg_notify(CAST('guide' AS text),CAST(NEW.id AS text));
    RETURN NEW;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION sync_guide()
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION sync_page()
  RETURNS trigger AS
$BODY$
DECLARE
BEGIN
    PERFORM pg_notify(CAST('page' AS text),CAST(NEW.id AS text));
    RETURN NEW;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION sync_page()
  OWNER TO postgres;

-- DROP TRIGGER sync ON guide;

CREATE TRIGGER sync
  BEFORE INSERT OR UPDATE
  ON guide
  FOR EACH ROW
  EXECUTE PROCEDURE sync_guide();

 -- DROP TRIGGER sync ON page;

CREATE TRIGGER sync
  AFTER INSERT OR UPDATE
  ON page
  FOR EACH ROW
  EXECUTE PROCEDURE sync_page();

