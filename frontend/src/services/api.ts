import type { IdCardOcrResult } from '../types/ocr';
import type {
  VendorFormData,
  VendorRecord,
  PaginatedVendorResponse
} from '../types/vendor';

const BASE_URL = '/api';

export async function scanIdCard(file: File): Promise<IdCardOcrResult> {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${BASE_URL}/ocr/scan-id-card`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Scan failed' }));
    throw new Error(errorData.detail || 'Failed to scan ID card');
  }

  return res.json();
}

export async function createVendor(data: VendorFormData): Promise<VendorRecord> {
  const res = await fetch(`${BASE_URL}/vendors`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to create vendor' }));
    throw new Error(err.detail || 'Failed to create vendor');
  }

  return res.json();
}

export async function listVendors(
  query: string = '',
  page: number = 1,
  limit: number = 10
): Promise<PaginatedVendorResponse> {
  const params = new URLSearchParams({
    page: String(page),
    limit: String(limit),
  });
  if (query.trim()) {
    params.set('query', query.trim());
  }

  const res = await fetch(`${BASE_URL}/vendors?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to load vendors');
  return res.json();
}

export async function getVendor(id: number): Promise<VendorRecord> {
  const res = await fetch(`${BASE_URL}/vendors/${id}`);
  if (!res.ok) throw new Error('Vendor not found');
  return res.json();
}

export async function deleteVendor(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/vendors/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete vendor');
}

export function getExcelExportUrl(id: number): string {
  return `${BASE_URL}/vendors/${id}/export-excel`;
}

export function getPdfExportUrl(id: number): string {
  return `${BASE_URL}/vendors/${id}/export-pdf`;
}
