package MicroUser.UserSpringBoot.Model;

import jakarta.persistence.*;

@Entity
public class K6Model {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private long timestamp;
    private boolean anomaly;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public boolean isAnomaly() {
        return anomaly;
    }

    public void setAnomaly(boolean isAnomaly) {
        this.anomaly = isAnomaly;
    }
}
