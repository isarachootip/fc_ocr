import React, { useState } from 'react';
import { CheckCircle } from 'lucide-react';
import { useAuth } from './hooks/useAuth';
import { isAdmin, isSysadmin } from './services/roles';
import { AppNav, type AppTab } from './components/layout/AppNav';
import { UsersView } from './components/users/UsersView';
import { SystemSettingsView } from './components/settings/SystemSettingsView';
import { ChangePasswordModal } from './components/auth/ChangePasswordModal';
import type { VendorFormData, VendorRecord } from './types/vendor';
import type { IdCardOcrResult } from './types/ocr';
import { OcrUploader } from './components/ocr/OcrUploader';
import { OcrConfirmModal } from './components/ocr/OcrConfirmModal';
import { VendorFormView } from './components/vendor-form/VendorFormView';
import { VendorListView } from './components/vendor-list/VendorListView';
import { A4PrintableView } from './components/print/A4PrintableView';

const INITIAL_FORM: VendorFormData = {
  vendor_name_th: '',
  tax_id: '',
  status_type: 'เพิ่มเติม',
  oracle_module: 'AP',
  branch_no: 'สำนักงานใหญ่',
  business_format: 'ซื้อมาขายไป',
  vat_type: 'ระบบภาษีมูลค่าเพิ่ม 7%',
  wht_type: 'ภ.ง.ด. 3',
  wht_rate: '3%',
  payment_term: 'โอนผ่านธนาคาร',
  fast_type: 'Supplier',
};

export const App: React.FC = () => {
  const { user, signOut } = useAuth();
  const [activeTab, setActiveTab] = useState<AppTab>('form');
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState<VendorFormData>({ ...INITIAL_FORM });
  const [ocrModalData, setOcrModalData] = useState<IdCardOcrResult | null>(null);
  const [printVendor, setPrintVendor] = useState<VendorRecord | null>(null);
  const [successBanner, setSuccessBanner] = useState<string | null>(null);

  const handleOcrConfirm = (confirmed: IdCardOcrResult) => {
    setFormData((prev) => ({
      ...prev,
      vendor_name_th: confirmed.full_name_th || prev.vendor_name_th,
      vendor_name_en: confirmed.full_name_en || prev.vendor_name_en,
      tax_id: confirmed.tax_id || prev.tax_id,
      address_no: confirmed.address_no || prev.address_no,
      address_moo: confirmed.address_moo || prev.address_moo,
      address_subdistrict: confirmed.address_subdistrict || prev.address_subdistrict,
      address_district: confirmed.address_district || prev.address_district,
      address_province: confirmed.address_province || prev.address_province,
      address_postcode: confirmed.address_postcode || prev.address_postcode,
      id_card_file_path: confirmed.file_path || prev.id_card_file_path,
    }));
    setOcrModalData(null);
    setSuccessBanner('ดึงข้อมูลจากบัตรประชาชนเข้าสู่แบบฟอร์มเรียบร้อยแล้ว');
  };

  const handleSaveSuccess = (vendor: VendorRecord) => {
    setSuccessBanner(`บันทึกข้อมูลเรียบร้อย! รหัสร้านค้า: ${vendor.vendor_code}`);
    setFormData({ ...INITIAL_FORM });
    setActiveTab('list');
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <AppNav
        user={user}
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        onOpenChangePassword={() => setShowPassword(true)}
        onSignOut={signOut}
      />

      <main className="max-w-6xl w-full mx-auto px-4 py-6 flex-1">
        {successBanner && (
          <div className="mb-5 p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-medium flex items-center justify-between">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-emerald-600" />
              <span>{successBanner}</span>
            </div>
            <button onClick={() => setSuccessBanner(null)} className="text-emerald-600 hover:underline">ปิด</button>
          </div>
        )}

        {activeTab === 'form' ? (
          <div>
            <OcrUploader onScanComplete={(res) => setOcrModalData(res)} />
            <VendorFormView
              formData={formData}
              setFormData={setFormData}
              onSaveSuccess={handleSaveSuccess}
              onReset={() => setFormData({ ...INITIAL_FORM })}
            />
          </div>
        ) : activeTab === 'users' && isAdmin(user.role) ? (
          <UsersView />
        ) : activeTab === 'settings' && isSysadmin(user.role) ? (
          <SystemSettingsView />
        ) : (
          <VendorListView onSelectPrint={(v) => setPrintVendor(v)} />
        )}
      </main>

      {ocrModalData && (
        <OcrConfirmModal
          data={ocrModalData}
          onConfirm={handleOcrConfirm}
          onClose={() => setOcrModalData(null)}
        />
      )}

      {showPassword && <ChangePasswordModal onClose={() => setShowPassword(false)} />}
      {printVendor && <A4PrintableView vendor={printVendor} onClose={() => setPrintVendor(null)} />}
    </div>
  );
};

export default App;
