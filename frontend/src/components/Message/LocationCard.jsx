import { useState } from 'react'
import { MapPin, ExternalLink, Map } from 'lucide-react'

export default function LocationCard({ location }) {
  const [mapOpen, setMapOpen] = useState(true)

  if (!location) return null

  const { name, block, floor, description, embed_map_url, search_map_url } = location

  return (
    <div className="location-card">
      <div className="location-card__header">
        <div className="location-card__title-row">
          <div className="location-card__icon-box">
            <MapPin size={20} strokeWidth={2.4} />
          </div>
          <div>
            <h4 className="location-card__name">{name}</h4>
            {block || floor ? (
              <div className="location-card__badges">
                {block ? <span className="badge badge--block">🏢 {block}</span> : null}
                {floor ? <span className="badge badge--floor">🪜 {floor}</span> : null}
              </div>
            ) : null}
          </div>
        </div>

        <div className="location-card__actions">
          {embed_map_url ? (
            <button
              type="button"
              className="location-card__toggle"
              onClick={() => setMapOpen((prev) => !prev)}
            >
              <Map size={14} strokeWidth={2} />
              <span>{mapOpen ? 'Hide Map' : 'Show Map'}</span>
            </button>
          ) : null}
          {search_map_url ? (
            <a
              href={search_map_url}
              target="_blank"
              rel="noopener noreferrer"
              className="location-card__btn"
            >
              <span>Open in Google Maps</span>
              <ExternalLink size={14} strokeWidth={2} />
            </a>
          ) : null}
        </div>
      </div>

      {description ? (
        <p className="location-card__desc">{description}</p>
      ) : null}

      {mapOpen && embed_map_url ? (
        <div className="location-card__map-wrap">
          <iframe
            title={`Map for ${name}`}
            src={embed_map_url}
            className="location-card__iframe"
            loading="lazy"
            allowFullScreen
            referrerPolicy="no-referrer-when-downgrade"
          />
        </div>
      ) : null}
    </div>
  )
}
