import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  MessageSquare, BookOpen, TrendingUp, Sprout,
  ArrowRight, AlertTriangle, CheckCircle, Leaf, Wheat
} from 'lucide-react';
import { cropsAPI, adminAPI } from '../api';

const CROP_ICONS = {
  Rice: '🌾', Wheat: '🌾', Tomato: '🍅', Potato: '🥔',
  Cotton: '☁️', Maize: '🌽', Groundnut: '🥜',
};

const SAMPLE_QUESTIONS = [
  { q: 'What are the symptoms of rice blast disease?', icon: '🔍' },
  { q: 'How can I prevent bacterial leaf blight?', icon: '🛡️' },
  { q: 'What causes tomato leaf curl?', icon: '🍃' },
  { q: 'Management methods for wheat rust?', icon: '⚕️' },
  { q: 'How to protect crops from fungal infections?', icon: '🧪' },
  { q: 'What are favorable conditions for potato late blight?', icon: '🌦️' },
];

function StatCard({ label, value, icon, color }) {
  return (
    <div className="card flex items-center gap-4">
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${color}`}>
        {icon}
      </div>
      <div>
        <div className="text-2xl font-bold text-gray-800">{value}</div>
        <div className="text-sm text-gray-500">{label}</div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [crops, setCrops] = useState([]);
  const [health, setHealth] = useState(null);

  useEffect(() => {
    cropsAPI.getCrops().then(r => setCrops(r.data.crops || [])).catch(() => {});
    adminAPI.health().then(r => setHealth(r.data)).catch(() => {});
  }, []);

  const totalDiseases = crops.reduce((sum, c) => sum + (c.disease_count || 0), 0);
  const llmAvailable = health?.rag?.llm_available;

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {/* Hero */}
      <div className="bg-gradient-to-br from-primary-800 via-primary-700 to-primary-600 
                      rounded-2xl p-8 text-white shadow-xl relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute -top-10 -right-10 w-60 h-60 bg-white rounded-full"></div>
          <div className="absolute -bottom-20 -left-10 w-80 h-80 bg-white rounded-full"></div>
        </div>
        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-3">
            <Leaf className="text-accent-300" size={20} />
            <span className="text-primary-200 text-sm font-medium">AI-Powered Agriculture</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold mb-3 leading-tight">
            Crop Disease Knowledge<br />
            <span className="text-accent-300">Assistant</span>
          </h1>
          <p className="text-primary-200 max-w-xl text-sm md:text-base leading-relaxed mb-6">
            Ask any question about crop diseases, symptoms, causes, prevention, and management 
            strategies. Our RAG-powered AI retrieves answers from trusted agricultural sources.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link to="/chat" className="btn-primary bg-accent-500 hover:bg-accent-600 text-primary-900 
                                       flex items-center gap-2 text-sm">
              <MessageSquare size={16} /> Start Chatting
            </Link>
            <Link to="/crops" className="btn-secondary border-primary-400 text-white hover:bg-primary-600
                                        flex items-center gap-2 text-sm">
              <BookOpen size={16} /> Browse Diseases
            </Link>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard label="Supported Crops" value={crops.length || 7}
          icon={<Sprout size={22} className="text-primary-700" />}
          color="bg-primary-100" />
        <StatCard label="Disease Profiles" value={totalDiseases || '15+'}
          icon={<AlertTriangle size={22} className="text-orange-600" />}
          color="bg-orange-100" />
        <StatCard label="Knowledge Chunks" value={health?.rag?.total_chunks || '—'}
          icon={<BookOpen size={22} className="text-blue-600" />}
          color="bg-blue-100" />
        <StatCard
          label="AI Status"
          value={llmAvailable == null ? '...' : llmAvailable ? 'Active' : 'Fallback'}
          icon={<CheckCircle size={22} className={llmAvailable ? 'text-green-600' : 'text-yellow-600'} />}
          color={llmAvailable ? 'bg-green-100' : 'bg-yellow-100'}
        />
      </div>

      {/* Crops + Sample Questions */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Supported Crops */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-bold text-gray-800 flex items-center gap-2">
              <Wheat size={18} className="text-primary-700" />
              Supported Crops
            </h2>
            <Link to="/crops" className="text-xs text-primary-600 hover:text-primary-800 
                                        flex items-center gap-1 font-medium">
              View all <ArrowRight size={12} />
            </Link>
          </div>
          <div className="grid grid-cols-2 gap-2">
            {(crops.length ? crops : ['Rice','Wheat','Tomato','Potato','Cotton','Maize','Groundnut']
              .map(n => ({ name: n, disease_count: 0 }))).map((crop) => (
              <Link
                key={crop.name}
                to={`/crops/${crop.name.toLowerCase()}`}
                className="flex items-center gap-3 p-3 rounded-xl bg-gray-50 hover:bg-primary-50 
                           border border-gray-100 hover:border-primary-200 transition-all group"
              >
                <span className="text-2xl">{CROP_ICONS[crop.name] || '🌿'}</span>
                <div>
                  <div className="text-sm font-semibold text-gray-700 group-hover:text-primary-700">
                    {crop.name}
                  </div>
                  <div className="text-xs text-gray-400">
                    {crop.disease_count > 0 ? `${crop.disease_count} diseases` : 'View diseases'}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Sample questions */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-bold text-gray-800 flex items-center gap-2">
              <MessageSquare size={18} className="text-primary-700" />
              Try Asking
            </h2>
            <Link to="/chat" className="text-xs text-primary-600 hover:text-primary-800 
                                       flex items-center gap-1 font-medium">
              Open Chat <ArrowRight size={12} />
            </Link>
          </div>
          <div className="space-y-2">
            {SAMPLE_QUESTIONS.map(({ q, icon }) => (
              <Link
                key={q}
                to={`/chat?q=${encodeURIComponent(q)}`}
                className="flex items-center gap-3 p-3 rounded-xl bg-gray-50 hover:bg-primary-50 
                           border border-gray-100 hover:border-primary-200 transition-all group"
              >
                <span className="text-lg shrink-0">{icon}</span>
                <span className="text-sm text-gray-700 group-hover:text-primary-700">{q}</span>
                <ArrowRight size={14} className="ml-auto text-gray-300 group-hover:text-primary-500 shrink-0" />
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* How it works */}
      <div className="card">
        <h2 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
          <TrendingUp size={18} className="text-primary-700" />
          How It Works — RAG Pipeline
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { step: 1, title: 'Your Question', desc: 'You ask about a crop disease', icon: '❓' },
            { step: 2, title: 'Embedding', desc: 'Question is converted to a vector', icon: '🔢' },
            { step: 3, title: 'Retrieval', desc: 'Relevant docs retrieved from FAISS', icon: '🔍' },
            { step: 4, title: 'AI Answer', desc: 'Gemini generates a grounded response', icon: '🤖' },
          ].map(({ step, title, desc, icon }) => (
            <div key={step} className="text-center p-4 rounded-xl bg-primary-50 border border-primary-100">
              <div className="text-2xl mb-2">{icon}</div>
              <div className="text-xs font-bold text-primary-600 uppercase tracking-wide mb-1">
                Step {step}
              </div>
              <div className="text-sm font-semibold text-gray-800 mb-1">{title}</div>
              <div className="text-xs text-gray-500">{desc}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Disclaimer */}
      {llmAvailable === false && (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex gap-3">
          <AlertTriangle size={20} className="text-amber-600 shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-semibold text-amber-800">Gemini API Key Not Configured</p>
            <p className="text-xs text-amber-700 mt-1">
              The chatbot is running in fallback mode (returns raw retrieved content). 
              Add your <code className="bg-amber-100 px-1 rounded">GEMINI_API_KEY</code> in the 
              backend <code className="bg-amber-100 px-1 rounded">.env</code> file for AI-generated responses.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

