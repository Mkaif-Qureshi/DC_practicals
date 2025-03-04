package common.src;

import java.io.Serializable;

public class FileChunk implements Serializable {
    private static final long serialVersionUID = 1L;
    private byte[] chunkData;
    private int chunkNumber;

    public FileChunk(byte[] chunkData, int chunkNumber) {
        this.chunkData = chunkData;
        this.chunkNumber = chunkNumber;
    }

    public byte[] getChunkData() {
        return chunkData;
    }

    public int getChunkNumber() {
        return chunkNumber;
    }
}
