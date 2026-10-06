export interface VendorFormData {
  // 1. ผู้ขอ
  req_date?: string;
  req_email?: string;
  req_name?: string;
  req_department?: string;
  req_bu?: string;
  req_phone?: string;
  req_ext?: string;

  // 2. ข้อมูลที่ขอเพิ่ม/ปรับปรุง
  status_type?: string;
  oracle_module?: string;
  purpose?: string;
  purpose_other?: string;
  checked_by?: string;
  check_date?: string;

  // 3. รายการปรับปรุง
  update_details?: string;

  // 4. ชื่อและที่อยู่
  vendor_name_th: string;
  vendor_name_en?: string;
  address_no?: string;
  address_moo?: string;
  address_building?: string;
  address_floor?: string;
  address_village?: string;
  address_soi?: string;
  address_road?: string;
  address_subdistrict?: string;
  address_district?: string;
  address_province?: string;
  address_postcode?: string;
  vendor_phone?: string;
  vendor_fax?: string;
  email_remittance?: string;
  fax_remittance?: string;
  email_etax?: string;

  // 5. ภาษี/บัตรประชาชน
  tax_id: string;
  branch_no?: string;

  // 6. ผู้ติดต่อ
  contact_name?: string;
  contact_phone?: string;
  contact_mobile?: string;
  contact_email?: string;

  // 7. รูปแบบการค้า
  business_format?: string;
  business_format_detail?: string;

  // 8. ภาษีมูลค่าเพิ่ม
  vat_type?: string;

  // 9. หัก ณ ที่จ่าย
  wht_type?: string;
  wht_rate?: string;
  property_billing_dept?: string;
  is_gov_agency?: boolean;
  ship_to_address?: string;

  // 10. เงื่อนไขชำระเงิน
  payment_term?: string;
  credit_days?: string;

  // 11. วิธีชำระเงิน
  payment_method?: string;

  // 12. ธนาคาร
  bank_name?: string;
  bank_branch?: string;
  bank_account_name_th?: string;
  bank_account_name_en?: string;
  bank_account_type?: string;
  bank_account_no?: string;

  // 13. เอกสารแนบ
  attached_docs?: string;

  // 14. FAST
  fast_type?: string;
  fast_site?: string;
  fast_terms?: string;
  fast_pay_group?: string;
  fast_branch?: string;
  fast_sub_account?: string;

  // 15. ลายเซ็น
  approver_requestor_name?: string;
  approver_requestor_date?: string;
  approver_manager_name?: string;
  approver_manager_date?: string;

  // แนบไฟล์
  id_card_file_path?: string;
}

export interface VendorRecord extends VendorFormData {
  id: number;
  vendor_code: string;
  created_at: string;
  created_by?: string | null;
  updated_at: string;
}

export interface VendorListItem {
  id: number;
  vendor_code: string;
  vendor_name_th: string;
  vendor_name_en?: string;
  tax_id: string;
  status_type?: string;
  oracle_module?: string;
  created_at: string;
  created_by?: string | null;
}

export interface PaginatedVendorResponse {
  items: VendorListItem[];
  total: number;
  page: number;
  limit: number;
}
