import React, { useState } from 'react';
import { Building2, ListFilter, PlusCircle, CheckCircle, LogOut } from 'lucide-react';
import { useAuth } from './hooks/useAuth';
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
  const [activeTab, setActiveTab] = useState<'form' | 'list'>('form');
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
      {/* Top Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-bold shadow-md shadow-indigo-100">
              <Building2 className="w-5 h-5" />
            </div>
            <div>
              <h1 className="font-bold text-slate-800 text-base">ระบบลงทะเบียนและจัดการ Vendor Master</h1>
              <p className="text-xs text-slate-500">พร้อมระบบอ่านบัตรประชาชนอัตโนมัติ (AI & Local OCR)</p>
            </div>
          </div>

          <div className="flex bg-slate-100 p-1 rounded-xl">
            <button
              onClick={() => setActiveTab('form')}
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
                activeTab === 'form' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <PlusCircle className="w-4 h-4" /> แบบฟอร์มเปิด Vendor
            </button>
            <button
              onClick={() => setActiveTab('list')}
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
                activeTab === 'list' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <ListFilter className="w-4 h-4" /> ทะเบียนผู้ค้า & พิมพ์เอกสาร
            </button>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-xs text-slate-500 hidden sm:inline">{user.username}</span>
            <button
              onClick={signOut}
              className="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-rose-600 hover:bg-rose-50 flex items-center gap-1.5 transition-colors"
            >
              <LogOut className="w-4 h-4" /> ออกจากระบบ
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
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
        ) : (
          <VendorListView onSelectPrint={(v) => setPrintVendor(v)} />
        )}
      </main>

      {/* OCR Review & Confirm Modal */}
      {ocrModalData && (
        <OcrConfirmModal
          data={ocrModalData}
          onConfirm={handleOcrConfirm}
          onClose={() => setOcrModalData(null)}
        />
      )}

      {/* A4 Printable View Modal */}
      {printVendor && (
        <A4PrintableView vendor={printVendor} onClose={() => setPrintVendor(null)} />
      )}
    </div>
  );
};

export default App;
