export interface IdCardOcrResult {
  tax_id: string;
  title_th?: string | null;
  first_name_th?: string | null;
  last_name_th?: string | null;
  full_name_th: string;

  title_en?: string | null;
  first_name_en?: string | null;
  last_name_en?: string | null;
  full_name_en?: string | null;

  date_of_birth_th?: string | null;
  date_of_birth_en?: string | null;

  address_raw?: string | null;
  address_no?: string | null;
  address_moo?: string | null;
  address_subdistrict?: string | null;
  address_district?: string | null;
  address_province?: string | null;
  address_postcode?: string | null;

  issue_date?: string | null;
  expiry_date?: string | null;
  file_path?: string | null;
  engine_used?: string | null;
}
