import React, { useState, useEffect } from 'react';
import { Search, FileSpreadsheet, FileText, Printer, Trash2, Loader2 } from 'lucide-react';
import type { VendorListItem, VendorRecord } from '../../types/vendor';
import { listVendors, deleteVendor, getExcelExportUrl, getPdfExportUrl, getVendor } from '../../services/api';

interface Props {
  onSelectPrint: (vendor: VendorRecord) => void;
}

export const VendorListView: React.FC<Props> = ({ onSelectPrint }) => {
  const [vendors, setVendors] = useState<VendorListItem[]>([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);

  const fetchVendors = async (searchQuery = '') => {
    setLoading(true);
    try {
      const res = await listVendors(searchQuery, 1, 50);
      setVendors(res.items);
      setTotal(res.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVendors();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchVendors(query);
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('คุณต้องการลบข้อมูลร้านค้านี้ใช่หรือไม่?')) return;
    try {
      await deleteVendor(id);
      fetchVendors(query);
    } catch (err) {
      alert('ลบข้อมูลไม่สำเร็จ');
    }
  };

  const handleOpenPrint = async (id: number) => {
    try {
      const fullVendor = await getVendor(id);
      onSelectPrint(fullVendor);
    } catch (err) {
      alert('ไม่สามารถโหลดข้อมูลสำหรับพิมพ์ได้');
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      {/* Search Header */}
      <div className="p-5 border-b border-slate-200 bg-slate-50/50 flex flex-col sm:flex-row justify-between items-center gap-3">
        <h3 className="font-bold text-slate-800 text-base">
          ทะเบียนร้านค้าในระบบ ({total} รายการ)
        </h3>
        <form onSubmit={handleSearch} className="flex gap-2 w-full sm:w-80">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="ค้นหารหัส, ชื่อ, หรือเลขบัตร..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 border border-slate-300 rounded-lg text-xs bg-white focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <button
            type="submit"
            className="px-3 py-1.5 bg-indigo-600 text-white rounded-lg text-xs font-semibold hover:bg-indigo-700"
          >
            ค้นหา
          </button>
        </form>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-100/70 text-slate-600 font-semibold">
              <th className="py-3 px-4">รหัสร้านค้า (Vendor Code)</th>
              <th className="py-3 px-4">ชื่อร้านค้า / บุคคล</th>
              <th className="py-3 px-4">เลขประจำตัว 13 หลัก</th>
              <th className="py-3 px-4">วันที่บันทึก</th>
              <th className="py-3 px-4 text-center">จัดการและพิมพ์เอกสาร</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {loading ? (
              <tr>
                <td colSpan={5} className="py-8 text-center text-slate-400">
                  <Loader2 className="w-6 h-6 animate-spin mx-auto mb-2" />
                  กำลังโหลดข้อมูล...
                </td>
              </tr>
            ) : vendors.length === 0 ? (
              <tr>
                <td colSpan={5} className="py-8 text-center text-slate-400">
                  ยังไม่มีข้อมูลผู้ค้าในระบบ
                </td>
              </tr>
            ) : (
              vendors.map((v) => (
                <tr key={v.id} className="hover:bg-slate-50 transition-colors">
                  <td className="py-3 px-4 font-mono font-bold text-indigo-700">{v.vendor_code}</td>
                  <td className="py-3 px-4 font-medium text-slate-900">{v.vendor_name_th}</td>
                  <td className="py-3 px-4 font-mono">{v.tax_id}</td>
                  <td className="py-3 px-4 text-slate-500">{new Date(v.created_at).toLocaleDateString('th-TH')}</td>
                  <td className="py-3 px-4">
                    <div className="flex items-center justify-center gap-1.5">
                      <button
                        onClick={() => handleOpenPrint(v.id)}
                        className="p-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-md"
                        title="พิมพ์ A4 หน้าเว็บ"
                      >
                        <Printer className="w-4 h-4" />
                      </button>
                      <a
                        href={getExcelExportUrl(v.id)}
                        download
                        className="p-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-md"
                        title="ดาวน์โหลด Excel แม่แบบ"
                      >
                        <FileSpreadsheet className="w-4 h-4" />
                      </a>
                      <a
                        href={getPdfExportUrl(v.id)}
                        target="_blank"
                        rel="noreferrer"
                        className="p-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-md"
                        title="พิมพ์ / ดาวน์โหลด PDF"
                      >
                        <FileText className="w-4 h-4" />
                      </a>
                      <button
                        onClick={() => handleDelete(v.id)}
                        className="p-1.5 hover:bg-red-50 text-slate-400 hover:text-red-600 rounded-md"
                        title="ลบ"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
