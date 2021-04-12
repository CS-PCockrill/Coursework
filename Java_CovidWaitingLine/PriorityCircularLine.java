public class PriorityCircularLine<T extends Comparable<T>> implements CircularLineInterface<T> {
  // data for circular line
  private T[] circularLine;
  private int capacity;
  private int size;
  private int start;
  private int end;

  /**
   * creates an empty array (circularLine) of default capacity 50.
   */
  public PriorityCircularLine() {
    // initialize object by calling other constructor.
    this(50);
  }

  /**
   * Creates an empty waiting line with parameter capacity
   * @param: capacity initial capacity of waiting line
   */
  public PriorityCircularLine(int capacity) {
    this.capacity = capacity;
    this.circularLine = (T[]) new Comparable[capacity];
    start = 0;
    end = capacity - 1;
    size = 0;

  }

  /**
   * will double the size of the existing waiting line if it is full
   * if it is not full then it will do nothing
   */
  public void doubleCapacity() {
    if (isFull()) {
      int fullCapacity = capacity;
      capacity *= 2;
      // create overflow array to accomodate new elements (double size of current list)
      T[] overflowCircularLine = (T[]) new Comparable[capacity];

      // copy each element from existing array
      for (int i=0; i < size; i++) {
        // elements need to be added in order, and the modulo makes sure that it
        // loops around to index 0 if (IndexOutOfBounds)
        int position = (start + i) % fullCapacity;
        overflowCircularLine[i] = circularLine[position];
      }
      // reassign overflow to existing waiting line
      circularLine = overflowCircularLine;
      // update start and end of new array
      start = 0;
      end = (start + (size - 1)) % capacity;
    }
    return;
  }

  /**
  * @return: position of start
  */
  public int getStart() {
    return start;
  }

  /**
  * @return: position of end
  */
  public int getEnd() {
    return end;
  }

  @Override
  public T getFront() {
    // check if the waiting line is empty, if so throw NoElementException
    if (isEmpty()) {
      throw new NoElementException();
    }

    return circularLine[start];
  }

  @Override
  public T getBack() {
    // check if the waiting line is empty, if so throw NoElementException
    if (isEmpty()) {
      throw new NoElementException();
    }
    return circularLine[end];
  }

  @Override
  public int getCapacity() {
    // due to social distancing capacity is 1 less. Leaving one spot unoccupied
    return capacity - 1;
  }

  @Override
  public boolean isFull() {
    return size == getCapacity();
  }

  @Override
  public boolean isEmpty() {
    // circularLine (waiting line) is empty if the size is 0;
    return size == 0;
  }

  @Override
  public int size() {
    return size;
  }

  /**
   * @return: returns the string representation of the waiting line separated by a comma
   */
  public String toString() {
    String waitingList = "[";
    for (int i=0; i<size; i++) {
      int position = (start + i) % capacity;
      // concat to waitingList String
      waitingList += circularLine[position].toString();
      // add comma if it is not the last name
      if (position != end) {
        waitingList += ",";
      }
    }
    return waitingList + "]";
  }

  @Override
  public void insert(T patient) {
    doubleCapacity();
    // check if an element has already been added by creating a boolean
    boolean isInserted = false;
    // we need to add patients based on priority, we start by looping from start position
    // and compare each element, and prioritize patients with a lower number
    // then put it in the front (lower priority)
    for (int i=0; i<size; i++) {
      int position = (start + i) % capacity;
      int validPos = circularLine[position].compareTo(patient);

      if (validPos > 0) {
        position = end;

        for (int j=0; j<(size - i); j++) {
          // index for the spot after (next position)
          int after = (position + 1) % capacity;
          circularLine[after] = circularLine[position];

          if (position == 0) {
            position = capacity;
          }
          position--;
          // all patients will be moved after these loop iterations
        }

        position = (position + 1) % capacity;
        // add new patient to the waiting line
        circularLine[position] = patient;
        // change the inserted flag to true
        isInserted = true;
        // patient is added in waiting line stop further searches
        break;
      }
    }
    if (!isInserted) {
      // update the end
      end = (end + 1) % capacity;
      // insert the new patient into the line
      circularLine[end] = patient;
    } else {
      end = (end + 1) % capacity;
    }
    // update number of patients in waiting line
    size++;
  }

  @Override
  public T remove() {
    // check if the line is empty;
    if (isEmpty()) {
      throw new NoElementException();
    }
    T tempStart = circularLine[start];
    // remove the element
    circularLine[start] = null;
    // update count of total people in line
    size--;
    // update first patient position
    start = (start + 1) % capacity;
    return tempStart;
  }

  @Override
  public void removeAll() {
    // check if the line is isEmpty
    if (isEmpty()) {
      throw new NoElementException();
    }
    // remove all people from circularLine
    for (int i=0; i<size; i++) {
      circularLine[i] = null;
    }
    // reset the start/end and size of line
    start = 0;
    end = capacity - 1;
    size = 0;
  }

}
