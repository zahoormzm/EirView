import { Camera, FileText, Image, Smartphone } from 'lucide-react';
import { useState } from 'react';
import FileUpload from '../components/FileUpload';
import ManualEntryForm from '../components/ManualEntryForm';
import useStore from '../store';
import { uploadAppleHealth, uploadFaceAge, uploadFile } from '../api';

const sources = [
  { key: 'blood_pdf', label: 'Blood Report', icon: FileText, accept: '.pdf' },
  { key: 'cultfit_image', label: 'Cult.fit Report', icon: Image, accept: '.png,.jpg,.jpeg' },
  { key: 'apple_health_xml', label: 'Apple Health', icon: Smartphone, accept: '.xml' },
  { key: 'face_age', label: 'Face Age Selfie', icon: Camera, accept: '.jpg,.jpeg,.png' }
];

export default function DataIngest() {
  const { selectedUserId } = useStore();
  const [selected, setSelected] = useState(sources[0]);
  const [result, setResult] = useState(null);
  const extracted = result?.extracted;

  const endpoint = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', selectedUserId);
    if (selected.key === 'face_age') return uploadFaceAge(formData);
    if (selected.key === 'apple_health_xml') return uploadAppleHealth(formData);
    formData.append('data_type', selected.key);
    return uploadFile(formData);
  };

  return (
    <div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {sources.map((source) => {
          const Icon = source.icon;
          return (
            <button key={source.key} onClick={() => setSelected(source)} className={`p-4 rounded-xl text-left ${selected.key === source.key ? 'ring-2 ring-emerald-500 bg-emerald-50' : 'bg-white border border-slate-200 hover:border-slate-300 cursor-pointer'}`}>
              <Icon size={20} className="text-slate-600" />
              <div className="font-medium text-slate-700 mt-3">{source.label}</div>
            </button>
          );
        })}
      </div>
      <FileUpload accept={selected.accept} label={selected.label} endpoint={endpoint} onUpload={setResult} />
      {selected.key === 'blood_pdf' && extracted?.source_summary && (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mt-6">
          <div className="flex flex-wrap items-center gap-3">
            <div className="text-sm font-semibold text-slate-800">Flexible Lab Extraction</div>
            <span className="text-xs rounded-full bg-emerald-50 text-emerald-700 px-2 py-1">{extracted.source_summary.tests_found} tests found</span>
            <span className="text-xs rounded-full bg-blue-50 text-blue-700 px-2 py-1">{extracted.source_summary.recognized_count} recognized</span>
            <span className="text-xs rounded-full bg-amber-50 text-amber-700 px-2 py-1">{extracted.source_summary.unmapped_count} unmapped</span>
          </div>
          {!!Object.keys(extracted.recognized_fields || {}).length && (
            <div className="mt-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">Profile Updates Applied</div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
                {Object.entries(extracted.recognized_fields).map(([key, value]) => (
                  <div key={key} className="rounded-lg bg-slate-50 border border-slate-200 px-3 py-2">
                    <div className="text-xs text-slate-500">{key.replaceAll('_', ' ')}</div>
                    <div className="text-sm font-medium text-slate-800 mt-1">{value ?? 'Not provided'}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {!!extracted.unmapped_tests?.length && (
            <div className="mt-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">Additional Tests Kept For Review</div>
              <div className="mt-2 text-sm text-slate-600">
                {extracted.unmapped_tests.map((item) => item.name).join(', ')}
              </div>
            </div>
          )}
          {!!extracted.missing_common_tests?.length && (
            <div className="mt-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">Common Tests Not Present In This Report</div>
              <div className="mt-2 text-sm text-slate-600">
                {extracted.missing_common_tests.join(', ')}
              </div>
            </div>
          )}
        </div>
      )}
      {result && (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mt-6">
          <pre className="text-xs text-slate-700 whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
      <div className="border-t border-slate-200 my-8" />
      <ManualEntryForm />
    </div>
  );
}
