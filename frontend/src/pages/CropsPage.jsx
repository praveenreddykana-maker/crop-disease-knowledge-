import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { cropsAPI } from '../api';
import { ArrowLeft, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react';

const CROP_ICONS = {
  rice: '🌾', wheat: '🌾', tomato: '🍅', potato: '🥔',
  cotton: '☁️', maize: '🌽', groundnut: '🥜',
};

const ALL_CROPS = ['Rice', 'Wheat', 'Tomato', 'Potato', 'Cotton', 'Maize', 'Groundnut'];

function DiseaseCard({ disease }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="card border border-gray-100 hover:border-primary-200 transition-all">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-start justify-between gap-3 text-left"
      >
        <div>
          <h3 className="font-bold text-gray-800 text-base">{disease.disease}</h3>
          <p className="text-sm text-gray-500 mt-0.5">{disease.pathogen}</p>
        </div>
        <div className="shrink-0 mt-1">
          {expanded ? <ChevronUp size={18} className="text-primary-600" /> : <ChevronDown size={18} className="text-gray-400" />}
        </div>
      </button>

      {expanded && (
        <div className="mt-4 space-y-4 border-t border-gray-100 pt-4 text-sm">
          {[
            { label: '🔴 Symptoms', value: disease.symptoms },
            { label: '🦠 Causes & Transmission', value: disease.causes },
            { label: '🌦️ Favorable Conditions', value: disease.favorable_conditions },
            { label: '🛡️ Prevention Methods', value: disease.prevention },
            { label: '⚕️ Management Recommendations', value: disease.management },
          ].map(({ label, value }) => (
            <div key={label}>
              <div className="font-semibold text-gray-700 mb-1">{label}</div>
              <p className="text-gray-600 leading-relaxed">{value}</p>
            </div>
          ))}
          <div className="bg-primary-50 border border-primary-100 rounded-lg p-3">
            <div className="font-semibold text-primary-800 text-xs uppercase tracking-wide mb-1">📚 Source</div>
            <div className="text-primary-700 text-xs">{disease.source}</div>
          </div>
          <div className="bg-amber-50 border border-amber-100 rounded-lg p-3 text-xs text-amber-800">
            ⚠️ Always consult your local agricultural extension service for crop-specific 
            chemical treatment recommendations.
          </div>
        </div>
      )}
    </div>
  );
}

function CropList() {
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Crop Disease Database</h1>
        <p className="text-gray-500 text-sm">
          Browse diseases organized by crop. Click any crop to view its disease profiles.
        </p>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {ALL_CROPS.map((crop) => (
          <Link
            key={crop}
            to={`/crops/${crop.toLowerCase()}`}
            className="card flex flex-col items-center gap-3 py-6 hover:border-primary-300 
                       hover:shadow-md transition-all group cursor-pointer text-center"
          >
            <span className="text-5xl">{CROP_ICONS[crop.toLowerCase()] || '🌿'}</span>
            <div>
              <div className="font-bold text-gray-800 group-hover:text-primary-700">{crop}</div>
              <div className="text-xs text-gray-400 mt-0.5">View diseases →</div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

function CropDiseases({ cropName }) {
  const [diseases, setDiseases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    cropsAPI.getCropDiseases(cropName)
      .then(r => {
        setDiseases(r.data.diseases || []);
        setLoading(false);
      })
      .catch(() => {
        setError(`No data found for ${cropName}`);
        setLoading(false);
      });
  }, [cropName]);

  const displayName = cropName.charAt(0).toUpperCase() + cropName.slice(1);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <Link to="/crops" className="text-gray-400 hover:text-primary-700 transition-colors">
          <ArrowLeft size={20} />
        </Link>
        <span className="text-3xl">{CROP_ICONS[cropName] || '🌿'}</span>
        <div>
          <h1 className="text-2xl font-bold text-gray-800">{displayName} Diseases</h1>
          <p className="text-gray-500 text-sm">{diseases.length} disease profiles</p>
        </div>
        <Link
          to={`/chat?q=Tell me about diseases in ${displayName}`}
          className="ml-auto btn-primary text-sm"
        >
          Ask AI About {displayName}
        </Link>
      </div>

      {loading && (
        <div className="text-center py-12 text-gray-400">Loading disease information...</div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex gap-3">
          <AlertCircle size={20} className="text-red-500" />
          <span className="text-red-700 text-sm">{error}</span>
        </div>
      )}

      {!loading && !error && (
        <div className="space-y-4">
          {diseases.map((disease, i) => (
            <DiseaseCard key={i} disease={disease} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function CropsPage() {
  const { cropName } = useParams();
  return cropName ? <CropDiseases cropName={cropName} /> : <CropList />;
}

