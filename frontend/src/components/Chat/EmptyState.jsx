import {
  BookOpen,
  IndianRupee,
  MapPin,
  Building2,
  Home,
  FileText,
  Calendar,
  PhoneCall,
  Sparkles,
  Compass,
  CornerDownRight,
  Check,
  ChevronRight,
} from 'lucide-react'
import campusHeroImg from '../../assets/daviet_campus_hero_transparent.png'

const EXPLORE_CATEGORIES = [
  {
    id: 'academics',
    title: 'Academics',
    subtitle: 'Courses, syllabus, exams',
    icon: BookOpen,
    iconColor: '#7c3aed',
    iconBg: '#ede4ff',
    prompt: 'What engineering programs, syllabus, and academic courses are offered at DAVIET?',
  },
  {
    id: 'fees',
    title: 'Fees',
    subtitle: 'Fee structure & payments',
    icon: IndianRupee,
    iconColor: '#059669',
    iconBg: '#d1fae5',
    prompt: 'What is the B.Tech fee structure and payment schedule as per IKG-PTU university guidelines?',
  },
  {
    id: 'location',
    title: 'Campus Location',
    subtitle: 'Find places & navigate',
    icon: MapPin,
    iconColor: '#e11d48',
    iconBg: '#ffe4e6',
    prompt: 'Where is the Training and Placement Office and Central Library on campus?',
  },
  {
    id: 'departments',
    title: 'Departments',
    subtitle: 'All engineering branches',
    icon: Building2,
    iconColor: '#2563eb',
    iconBg: '#dbeafe',
    prompt: 'Tell me about the Computer Science and other Engineering Departments at DAVIET.',
  },
  {
    id: 'hostel',
    title: 'Hostel Life',
    subtitle: 'Facilities, rules, rooms',
    icon: Home,
    iconColor: '#9333ea',
    iconBg: '#f3e8ff',
    prompt: 'What hostel facilities, mess timings, and accommodation options are available for students?',
  },
  {
    id: 'admissions',
    title: 'Admissions',
    subtitle: 'Eligibility, process, forms',
    icon: FileText,
    iconColor: '#ea580c',
    iconBg: '#ffedd5',
    prompt: 'What is the admission procedure, eligibility criteria, and intake for DAVIET?',
  },
  {
    id: 'timetable',
    title: 'Timetable',
    subtitle: 'Classes & academic calendar',
    icon: Calendar,
    iconColor: '#0284c7',
    iconBg: '#e0f2fe',
    prompt: 'What are the college working hours, class timetable patterns, and academic calendar dates?',
  },
  {
    id: 'contact',
    title: 'Contact Us',
    subtitle: 'Important numbers & offices',
    icon: PhoneCall,
    iconColor: '#c026d3',
    iconBg: '#fae8ff',
    prompt: 'What are the official contact numbers, email addresses, and administration office details of DAVIET?',
  },
]

export default function EmptyState({ onSelectPrompt }) {
  return (
    <div className="empty-state">
      {/* Hero Section with Campus Silhouette Illustration */}
      <div className="empty-state__hero-card">
        <div className="empty-state__hero-left">
          {/* Status pill */}
          <div className="hero-status-pill">
            <span className="hero-status-dot" />
            <span className="hero-status-label">Online</span>
            <span className="hero-status-divider">•</span>
            <span className="hero-status-sub">College Knowledge Assistant</span>
          </div>

          {/* Sparkle Icon Halo + Title */}
          <div className="hero-heading-group">
            <div className="hero-sparkle-halo">
              <Sparkles className="hero-sparkle-svg" size={28} />
            </div>
            <h1 className="hero-main-title">
              Hello, I&apos;m <span className="hero-brand-name">DAVIET Campus AI</span>
            </h1>
          </div>

          <p className="hero-description">
            Your intelligent guide to DAVIET campus, academics, fees, departments, hostel life and more.
          </p>

          {/* Feature Badges */}
          <div className="hero-badges-row">
            <div className="hero-pill-badge">
              <Check size={14} className="hero-pill-check" strokeWidth={3} />
              <span>College Information</span>
            </div>
            <div className="hero-pill-badge">
              <Check size={14} className="hero-pill-check" strokeWidth={3} />
              <span>Academic Guidance</span>
            </div>
            <div className="hero-pill-badge">
              <Check size={14} className="hero-pill-check" strokeWidth={3} />
              <span>Campus Assistance</span>
            </div>
          </div>
        </div>

        {/* Campus Illustration Right Column */}
        <div className="empty-state__hero-artwork">
          <img
            src={campusHeroImg}
            alt="DAVIET College Campus Illustration"
            className="hero-campus-image"
          />
        </div>
      </div>

      {/* Explore DAVIET Section */}
      <div className="empty-state__explore-section">
        <div className="explore-header-row">
          <div className="explore-title-box">
            <Compass size={19} strokeWidth={2.4} className="explore-compass-icon" />
            <h3 className="explore-title">Explore DAVIET</h3>
          </div>
          <span className="explore-curved-hint">
            Quick access to what you need <CornerDownRight size={14} className="explore-hint-arrow" />
          </span>
        </div>

        {/* 8 Clean Cards Grid */}
        <div className="explore-cards-grid">
          {EXPLORE_CATEGORIES.map((card) => {
            const IconComp = card.icon
            return (
              <button
                key={card.id}
                type="button"
                className="explore-card"
                onClick={() => onSelectPrompt?.(card.prompt)}
              >
                <div className="explore-card__top">
                  <div
                    className="explore-card__icon-wrap"
                    style={{ background: card.iconBg, color: card.iconColor }}
                  >
                    <IconComp size={19} strokeWidth={2.2} />
                  </div>
                  <ChevronRight size={16} className="explore-card__chevron" />
                </div>
                <div className="explore-card__content">
                  <h4 className="explore-card__title">{card.title}</h4>
                  <p className="explore-card__subtitle">{card.subtitle}</p>
                </div>
              </button>
            )
          })}
        </div>
      </div>
    </div>
  )
}
