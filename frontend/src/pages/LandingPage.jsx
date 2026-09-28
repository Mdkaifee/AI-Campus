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
  Bot,
  ArrowRight,
  Sun,
  Moon,
  ShieldCheck,
  Award,
  Users,
  GraduationCap,
  ExternalLink,
  LogIn,
  LogOut,
  UserCheck,
} from 'lucide-react'
import campusHeroImg from '../assets/daviet_campus_hero_transparent.png'
import { useAuth } from '../context/AuthContext'

const EXPLORE_TOPICS = [
  {
    id: 'academics',
    title: 'Academics & Courses',
    subtitle: 'B.Tech, M.Tech, MBA, MCA, syllabus & PTU regulations',
    icon: BookOpen,
    iconColor: '#7c3aed',
    iconBg: '#ede4ff',
    prompt: 'What engineering programs, syllabus, and academic courses are offered at DAVIET?',
  },
  {
    id: 'fees',
    title: 'Fee Structure',
    subtitle: 'Tuition fees, semester payments & university charges',
    icon: IndianRupee,
    iconColor: '#059669',
    iconBg: '#d1fae5',
    prompt: 'What is the B.Tech fee structure and payment schedule as per IKG-PTU university guidelines?',
  },
  {
    id: 'location',
    title: 'Campus Navigation',
    subtitle: 'Knowledge Centre, TPO, Auditorium, R&D & Core Block',
    icon: MapPin,
    iconColor: '#e11d48',
    iconBg: '#ffe4e6',
    prompt: 'Where is the Training and Placement Office and Central Library on campus?',
  },
  {
    id: 'departments',
    title: 'Departments & Labs',
    subtitle: 'CSE, AI & ML, ECE, EE, ME, CE & Applied Sciences',
    icon: Building2,
    iconColor: '#2563eb',
    iconBg: '#dbeafe',
    prompt: 'Tell me about the Computer Science and other Engineering Departments at DAVIET.',
  },
  {
    id: 'hostel',
    title: 'Hostels & Mess',
    subtitle: 'Sutlej, Beas & Raavi hostels, mess menu & security',
    icon: Home,
    iconColor: '#9333ea',
    iconBg: '#f3e8ff',
    prompt: 'What hostel facilities, mess timings, and accommodation options are available for students?',
  },
  {
    id: 'admissions',
    title: 'Admissions 2026',
    subtitle: 'Eligibility criteria, annual intake & registration',
    icon: FileText,
    iconColor: '#ea580c',
    iconBg: '#ffedd5',
    prompt: 'What is the admission procedure, eligibility criteria, and intake for DAVIET?',
  },
  {
    id: 'timetable',
    title: 'Hours & Timetable',
    subtitle: 'Working hours (9 AM - 5 PM), lecture slots & library',
    icon: Calendar,
    iconColor: '#0284c7',
    iconBg: '#e0f2fe',
    prompt: 'What are the college working hours, class timetable patterns, and academic calendar dates?',
  },
  {
    id: 'contact',
    title: 'Contacts & Helpline',
    subtitle: 'Principal office, TPO, anti-ragging & emails',
    icon: PhoneCall,
    iconColor: '#c026d3',
    iconBg: '#fae8ff',
    prompt: 'What are the official contact numbers, email addresses, and administration office details of DAVIET?',
  },
]

export default function LandingPage({ onOpenChat, theme, onToggleTheme }) {
  const isDark = theme === 'dark'
  const { user, openAuthModal, logout } = useAuth()

  return (
    <div className="landing-page">
      {/* Top Navbar */}
      <header className="landing-navbar">
        <div className="landing-navbar__inner">
          <div className="landing-brand">
            <div className="landing-brand__emblem">DAV</div>
            <div className="landing-brand__text">
              <span className="landing-brand__name">DAVIET Jalandhar</span>
              <span className="landing-brand__sub">Smart Campus Portal</span>
            </div>
          </div>

          <nav className="landing-nav-links">
            <a href="#about" className="landing-nav-link">About</a>
            <a href="#explore" className="landing-nav-link">Academics</a>
            <a href="#facilities" className="landing-nav-link">Facilities</a>
            <a href="https://davietjal.org" target="_blank" rel="noopener noreferrer" className="landing-nav-link external">
              Official Portal <ExternalLink size={13} />
            </a>
          </nav>

          <div className="landing-nav-actions">
            <button
              type="button"
              className="landing-theme-toggle"
              onClick={onToggleTheme}
              aria-label="Toggle theme"
            >
              {isDark ? <Sun size={18} /> : <Moon size={18} />}
            </button>

            {user ? (
              <div className="landing-user-profile">
                <div className="landing-user-chip" title={user.email}>
                  <div className="landing-user-avatar">
                    {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
                  </div>
                  <div className="landing-user-details">
                    <span className="landing-user-name">{user.name}</span>
                    <span className="landing-user-role">Student</span>
                  </div>
                </div>
                <button
                  type="button"
                  className="landing-logout-btn"
                  onClick={logout}
                  title="Sign out of account"
                >
                  <LogOut size={16} />
                  <span className="landing-logout-text">Sign Out</span>
                </button>
              </div>
            ) : (
              <div className="landing-auth-buttons">
                <button
                  type="button"
                  className="landing-signin-btn"
                  onClick={() => openAuthModal('login')}
                >
                  <LogIn size={15} />
                  <span>Sign In</span>
                </button>
                <button
                  type="button"
                  className="landing-signup-btn"
                  onClick={() => openAuthModal('signup')}
                >
                  <span>Sign Up</span>
                </button>
              </div>
            )}

            <button
              type="button"
              className="landing-cta-btn"
              onClick={() => onOpenChat?.()}
            >
              <Sparkles size={16} />
              <span>Ask Campus AI</span>
            </button>
          </div>
        </div>
      </header>

      <main className="landing-content">
        {/* Hero Section */}
        <section className="landing-hero">
          <div className="landing-hero__grid">
            <div className="landing-hero__text">
              <div className="landing-pill">
                <span className="landing-pill__dot" />
                <span>AI-Powered Smart Campus</span>
                <span className="landing-pill__sep">•</span>
                <span>IKG-PTU Affiliated</span>
              </div>

              <h1 className="landing-hero__title">
                DAV Institute of Engineering &amp; Technology
              </h1>

              <p className="landing-hero__desc">
                {user ? (
                  <>Welcome back, <strong>{user.name}</strong>! Your chat sessions and questions are securely saved to your student profile. Ask about courses, exams, fees, or faculty anytime.</>
                ) : (
                  <>Welcome to the next-generation DAVIET Smart Campus Portal. Explore programs, fee structures, admissions, and get instant verified answers from our AI Assistant 24/7.</>
                )}
              </p>

              <div className="landing-hero__actions">
                <button
                  type="button"
                  className="landing-btn-primary"
                  onClick={() => onOpenChat?.()}
                >
                  <Bot size={18} />
                  <span>Chat with Campus AI</span>
                  <ArrowRight size={16} />
                </button>

                {!user && (
                  <button
                    type="button"
                    className="landing-btn-secondary"
                    onClick={() => openAuthModal('signup')}
                  >
                    <UserCheck size={16} />
                    <span>Create Free Account</span>
                  </button>
                )}

                <a href="#explore" className="landing-btn-secondary">
                  <span>Explore Academics</span>
                </a>
              </div>

              <div className="landing-badges">
                <div className="landing-badge">
                  <Award size={15} className="landing-badge-icon" />
                  <span>NAAC Accredited</span>
                </div>
                <div className="landing-badge">
                  <ShieldCheck size={15} className="landing-badge-icon" />
                  <span>AICTE Approved</span>
                </div>
                <div className="landing-badge">
                  <GraduationCap size={15} className="landing-badge-icon" />
                  <span>IKG-PTU Affiliation</span>
                </div>
              </div>
            </div>

            <div className="landing-hero__visual">
              <div className="landing-hero__glow" />
              <img
                src={campusHeroImg}
                alt="DAVIET Campus Building Illustration"
                className="landing-hero__image"
              />
            </div>
          </div>
        </section>

        {/* Quick Stats Bar */}
        <section className="landing-stats">
          <div className="landing-stats__inner">
            <div className="landing-stat-card">
              <span className="stat-number">24+</span>
              <span className="stat-label">Years of Excellence</span>
            </div>
            <div className="landing-stat-card">
              <span className="stat-number">6+</span>
              <span className="stat-label">Engineering Streams</span>
            </div>
            <div className="landing-stat-card">
              <span className="stat-number">1200+</span>
              <span className="stat-label">Auditorium Capacity</span>
            </div>
            <div className="landing-stat-card">
              <span className="stat-number">24/7</span>
              <span className="stat-label">AI Campus Assistance</span>
            </div>
          </div>
        </section>

        {/* Explore DAVIET Grid */}
        <section id="explore" className="landing-explore">
          <div className="landing-section-header">
            <h2 className="landing-section-title">Explore DAVIET &amp; Ask Instant Questions</h2>
            <p className="landing-section-subtitle">
              Click any topic to launch the AI Assistant with instant answers from verified college records.
            </p>
          </div>

          <div className="landing-grid">
            {EXPLORE_TOPICS.map((topic) => {
              const IconComp = topic.icon
              return (
                <div
                  key={topic.id}
                  className="landing-card"
                  onClick={() => onOpenChat?.(topic.prompt)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      onOpenChat?.(topic.prompt)
                    }
                  }}
                >
                  <div
                    className="landing-card__icon"
                    style={{ background: topic.iconBg, color: topic.iconColor }}
                  >
                    <IconComp size={22} strokeWidth={2.2} />
                  </div>
                  <h3 className="landing-card__title">{topic.title}</h3>
                  <p className="landing-card__subtitle">{topic.subtitle}</p>
                  <div className="landing-card__action">
                    <span>Ask AI</span>
                    <ArrowRight size={14} />
                  </div>
                </div>
              )
            })}
          </div>
        </section>

        {/* About DAVIET Section */}
        <section id="about" className="landing-about">
          <div className="landing-about__inner">
            <div className="landing-about__card">
              <h2 className="landing-about__title">About DAVIET, Jalandhar</h2>
              <p className="landing-about__text">
                DAV Institute of Engineering &amp; Technology (DAVIET) was established in 2001 under the aegis of the DAV College Managing Committee (DAVCMC), New Delhi — the largest non-governmental educational organization in India.
              </p>
              <p className="landing-about__text">
                Situated in Kabir Nagar, Jalandhar, Punjab, the institute offers undergraduate and postgraduate programmes in Computer Science, AI &amp; ML, Electronics, Electrical, Mechanical, and Civil Engineering, approved by AICTE and affiliated to I.K. Gujral Punjab Technical University (IKG-PTU).
              </p>
              <div className="landing-about__links">
                <a
                  href="https://davietjal.org"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="landing-btn-secondary"
                >
                  Visit Official Website <ExternalLink size={14} />
                </a>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Floating Chat Trigger Button */}
      <button
        type="button"
        className="landing-floating-chat"
        onClick={() => onOpenChat?.()}
        aria-label="Open AI Assistant"
      >
        <div className="floating-chat-icon">
          <Bot size={22} />
          <span className="floating-chat-dot" />
        </div>
        <span className="floating-chat-text">Ask DAVIET AI</span>
      </button>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="landing-footer__inner">
          <p>© {new Date().getFullYear()} DAV Institute of Engineering &amp; Technology, Jalandhar. All rights reserved.</p>
          <p className="landing-footer__sub">Kabir Nagar, Jalandhar, Punjab 144008 • Approved by AICTE • Affiliated to IKG-PTU</p>
        </div>
      </footer>
    </div>
  )
}
