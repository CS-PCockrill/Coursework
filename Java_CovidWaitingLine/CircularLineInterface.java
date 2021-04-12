public interface CircularLineInterface<T> {
  // insert person
  public void insert(T newData);

  // Remove functions
  public T remove();
  public void removeAll();

  public T getFront();
  public T getBack();

  public int getCapacity();
  public int size();

  public boolean isEmpty();
  public boolean isFull();
}
