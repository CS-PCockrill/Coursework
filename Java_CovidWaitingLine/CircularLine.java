public class CircularLine<T> implements CircularLineInterface<T> {
  // initial waiting line data fields
  private T[] circularLine;
  private int capacity;
  private static int size ;
  private int start;
  private int end;

  /**
   * constructs a Circular line with default capacity 50.
   */
  public CircularLine() {
    // create an empty circularLine with a default capacity of 50.
    this(50);
  }

  /**
   * constructs a Circular line with a given capacity parameter.
   * @param: capacity is initial capacity of waiting line
   */
  public CircularLine(int capacity) {
    // initialize data
    this.capacity = capacity;
    circularLine = (T[]) new Object[capacity];
    this.size = 0;
    this.start = 0;
    // remove 1 from capacity as counting starts at 0
    this.end = capacity - 1;

  }

  /**
   * This method will double the capacity of circularLine if full. 
   * it will not execute when it is not full.
   */
  public void doubleCapacity() {
    if (isFull()) {
      int fullCapacity = capacity;
      capacity *= 2;
      // create new array that is double the size of existing capacity
      T[] overflowCircularLine = (T[]) new Object[capacity];
      // copy each element from existing line to overflow line
      for (int i=0; i < size; i++) {
        int position = (start + i) % fullCapacity;
        overflowCircularLine[i] = circularLine[position];
      }
      // reassign existing line to overflow line
      circularLine = overflowCircularLine;
      // update start and end
      start = 0;
      end = (start + size - 1) % capacity;
    }
    // this doubles the size of the CircularLine, if it is full.
    // existing elements should not be lost during resizing
    return;
  }

  /**
   * @return: position of start
   */
  public int getStart() {
    // returns the position of start
    return start;
  }

  /**
   * @return: position of end
   */
  public int getEnd() {
    // returns the position of end
    return end;
  }

  @Override
  public T getFront() {
    // Check if the line is empty
    if (isEmpty()) {
      throw new NoElementException();
    }
    return circularLine[start];
  }

  @Override
  public T getBack() {
    // Check if the line is empty
    if (isEmpty()) {
      throw new NoElementException();
    }
    return circularLine[end];
  }

  @Override
  public int getCapacity() {
    // due to social distancing we leave one spot unoccupied so therefore...
    return capacity - 1;
  }

  @Override
  public boolean isFull() {
    // check if the waiting line is full
    return size == getCapacity();
  }

  @Override
  public boolean isEmpty() {
    // check if the waiting line is empty
    return size == 0;
  }

  @Override
  public int size() {
    // return the size/amount of objects (non-null) in waiting line
    return size;
  }

  /**
   * @return: will return the string representation of the patients in the waiting line.
   */
  public String toString() {
    // Start building waitingList
    String waitingList = "[";
    // iterate to get every object on waiting list (circularLine)
    for (int i=0; i < size; i++) {
      // modulo for circular waiting line
      int position = (start + i) % capacity;
      waitingList = waitingList + circularLine[position].toString();

      // concat a comma if not end of line
      if (position != end) {
        waitingList += ",";
      }
    }

    return waitingList + "]";
  }

  @Override
  public void insert(T newData) {
    // Make sure its not full by calling doubleCapacity(). If it is full, the method
    // will double the capacity
    doubleCapacity();
    end = (end + 1) % capacity;
    // add new patient into circularLine
    circularLine[end] = newData;
    // update number of patients in circularLine
    size++;
  }

  @Override
  public T remove() {
    if (size == 0) {
      throw new NoElementException();
    }

    T tempStart = circularLine[start];
    circularLine[start] = null;
    size--;
    start = (start + 1) % capacity;

    return tempStart;
  }

  @Override
  public void removeAll() {
    // check if the waiting line is empty, if it is throw NoElementException
    if (isEmpty()) {
      throw new NoElementException();
    }
    for (int i=0; i < capacity; i++) {
      circularLine[i] = null;
    }
    start = 0;
    end = capacity - 1; // 1 less than capacity since 0 based counting
    size = 0; // removed all elements so size is now 0
  }
}
